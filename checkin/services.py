from dataclasses import dataclass
from datetime import datetime, time, timedelta
from decimal import Decimal

from django.db import transaction
from django.utils import timezone

from checkin.models.checkin import CoinTransaction, CoinWallet, cut_coin, gps, user_cut_coin


BASE_CHECKIN_COINS = 10
STREAK_BONUS_PER_DAY = 2
MAX_STREAK_BONUS = 20


class CoinError(ValueError):
    pass


class InsufficientCoins(CoinError):
    pass


@dataclass
class CoinAwardResult:
    awarded: bool
    amount: int
    streak_day: int
    balance_after: int
    already_awarded_today: bool = False


def calculate_checkin_reward(streak_day):
    streak_bonus = min(max(streak_day - 1, 0) * STREAK_BONUS_PER_DAY, MAX_STREAK_BONUS)
    return BASE_CHECKIN_COINS + streak_bonus


def get_coin_wallet(user):
    wallet, _ = CoinWallet.objects.get_or_create(user=user)
    return wallet


def get_checkin_local_date(checkin):
    return timezone.localtime(checkin.created_at).date()


def get_day_bounds(day):
    current_timezone = timezone.get_current_timezone()
    start = timezone.make_aware(datetime.combine(day, time.min), current_timezone)
    return start, start + timedelta(days=1)


def user_has_daily_reward(user, day, exclude_checkin_id=None):
    start, end = get_day_bounds(day)
    queryset = gps.objects.filter(
        user=user,
        coin_awarded=True,
        created_at__gte=start,
        created_at__lt=end,
    )
    if exclude_checkin_id:
        queryset = queryset.exclude(id=exclude_checkin_id)
    return queryset.exists()


def award_daily_checkin_coins(checkin):
    with transaction.atomic():
        checkin = gps.objects.select_for_update().select_related("user").get(pk=checkin.pk)
        wallet, _ = CoinWallet.objects.select_for_update().get_or_create(user=checkin.user)
        checkin_day = get_checkin_local_date(checkin)

        if checkin.coin_awarded:
            return CoinAwardResult(
                awarded=True,
                amount=checkin.coins_awarded,
                streak_day=checkin.streak_day,
                balance_after=wallet.balance,
            )

        if wallet.last_checkin_date == checkin_day or user_has_daily_reward(
            checkin.user,
            checkin_day,
            exclude_checkin_id=checkin.id,
        ):
            checkin.coin_awarded = False
            checkin.coins_awarded = 0
            checkin.streak_day = wallet.current_streak
            checkin.save(update_fields=["coin_awarded", "coins_awarded", "streak_day", "updated_at"])
            return CoinAwardResult(
                awarded=False,
                amount=0,
                streak_day=wallet.current_streak,
                balance_after=wallet.balance,
                already_awarded_today=True,
            )

        if wallet.last_checkin_date == checkin_day - timedelta(days=1):
            streak_day = wallet.current_streak + 1
        else:
            streak_day = 1

        amount = calculate_checkin_reward(streak_day)
        wallet.balance += amount
        wallet.current_streak = streak_day
        wallet.longest_streak = max(wallet.longest_streak, streak_day)
        wallet.last_checkin_date = checkin_day
        wallet.total_earned += amount
        wallet.save(
            update_fields=[
                "balance",
                "current_streak",
                "longest_streak",
                "last_checkin_date",
                "total_earned",
                "updated_at",
            ]
        )

        checkin.coin_awarded = True
        checkin.coins_awarded = amount
        checkin.streak_day = streak_day
        checkin.save(update_fields=["coin_awarded", "coins_awarded", "streak_day", "updated_at"])

        note = "เช็คอินต่อเนื่อง %s วัน" % streak_day
        CoinTransaction.objects.create(
            user=checkin.user,
            wallet=wallet,
            checkin=checkin,
            transaction_type=CoinTransaction.TYPE_CHECKIN,
            amount=amount,
            balance_after=wallet.balance,
            streak_day=streak_day,
            note=note,
        )

        return CoinAwardResult(
            awarded=True,
            amount=amount,
            streak_day=streak_day,
            balance_after=wallet.balance,
        )


def redeem_activity_reward(user, reward):
    if not reward.status:
        raise CoinError("รายการแลกนี้ปิดใช้งานแล้ว")

    cost = int(reward.coin or 0)
    if cost <= 0:
        raise CoinError("จำนวนเหรียญของรายการแลกไม่ถูกต้อง")

    hours = Decimal(reward.activity_hours or 0)

    with transaction.atomic():
        wallet, _ = CoinWallet.objects.select_for_update().get_or_create(user=user)
        if wallet.balance < cost:
            raise InsufficientCoins("เหรียญไม่พอสำหรับแลกรายการนี้")

        wallet.balance -= cost
        wallet.total_spent += cost
        wallet.activity_hours += hours
        wallet.save(update_fields=["balance", "total_spent", "activity_hours", "updated_at"])

        redemption = user_cut_coin.objects.create(
            user=user,
            cut_coin=reward,
            last_coin=wallet.balance,
            coin_spent=cost,
            activity_hours=hours,
            balance_after=wallet.balance,
            status="approved",
        )
        CoinTransaction.objects.create(
            user=user,
            wallet=wallet,
            redemption=redemption,
            transaction_type=CoinTransaction.TYPE_REDEEM,
            amount=-cost,
            balance_after=wallet.balance,
            note="แลก %s ชั่วโมงกิจกรรม" % hours,
        )
        return redemption


def rebuild_checkin_rewards_for_user(user):
    with transaction.atomic():
        CoinTransaction.objects.filter(
            user=user,
            transaction_type=CoinTransaction.TYPE_CHECKIN,
        ).delete()
        gps.objects.filter(user=user).update(
            coin_awarded=False,
            coins_awarded=0,
            streak_day=0,
        )
        wallet, _ = CoinWallet.objects.select_for_update().get_or_create(user=user)
        wallet.balance = 0
        wallet.current_streak = 0
        wallet.longest_streak = 0
        wallet.last_checkin_date = None
        wallet.total_earned = 0
        wallet.total_spent = 0
        wallet.activity_hours = Decimal("0")
        wallet.save()

    for checkin in gps.objects.filter(user=user).order_by("created_at", "id"):
        award_daily_checkin_coins(checkin)

    return get_coin_wallet(user)


def ensure_default_activity_rewards():
    rewards = [
        {
            "title": "แลก 1 ชั่วโมงกิจกรรม",
            "coin": 100,
            "activity_hours": Decimal("1.0"),
            "etc": "ใช้สำหรับบันทึกชั่วโมงกิจกรรมทั่วไป",
        },
        {
            "title": "แลก 2 ชั่วโมงกิจกรรม",
            "coin": 180,
            "activity_hours": Decimal("2.0"),
            "etc": "เหมาะกับผู้ที่เช็คอินต่อเนื่องหลายวัน",
        },
        {
            "title": "แลก 5 ชั่วโมงกิจกรรม",
            "coin": 420,
            "activity_hours": Decimal("5.0"),
            "etc": "แพ็กใหญ่สำหรับผู้ที่สะสมเหรียญระยะยาว",
        },
    ]
    created_or_updated = []
    for data in rewards:
        reward, _ = cut_coin.objects.update_or_create(
            title=data["title"],
            defaults={
                "coin": data["coin"],
                "activity_hours": data["activity_hours"],
                "etc": data["etc"],
                "status": True,
            },
        )
        created_or_updated.append(reward)
    return created_or_updated
