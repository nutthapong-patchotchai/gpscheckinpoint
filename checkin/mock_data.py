from collections import Counter
from datetime import date, datetime
from decimal import Decimal

from django.contrib.auth.models import User
from django.db import transaction
from django.utils import timezone

from checkin.models.address import Amphur, District, Geography, Province
from checkin.models.checkin import CoinTransaction, CovidCase, gps, point, user_cut_coin
from checkin.models.user import profile
from checkin.services import (
    ensure_default_activity_rewards,
    get_coin_wallet,
    rebuild_checkin_rewards_for_user,
    redeem_activity_reward,
)
from dormitory.models import About, Choice, Dorm, DormDetail, DormImage, DormOwner, DormStyle, UserDorm


TIMELINE_MOCK_TAG = "[timeline-mock]"
DEMO_MOCK_TAG = "[demo-data]"
DEMO_PASSWORD = "demo123456"


def first_or_create(model, lookup, defaults=None):
    instance = model.objects.filter(**lookup).first()
    if instance:
        return instance, False
    values = dict(defaults or {})
    values.update(lookup)
    return model.objects.create(**values), True


def aware_datetime(year, month, day, hour, minute):
    current_timezone = timezone.get_current_timezone()
    return timezone.make_aware(
        datetime(year, month, day, hour, minute),
        current_timezone,
    )


def ensure_mock_user(
    username,
    first_name,
    last_name,
    email="",
    is_staff=False,
    is_superuser=False,
    password=None,
):
    user, created = User.objects.get_or_create(
        username=username,
        defaults={
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "is_staff": is_staff,
            "is_superuser": is_superuser,
            "is_active": True,
        },
    )
    dirty = False
    for field, value in {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "is_staff": is_staff,
        "is_superuser": is_superuser,
        "is_active": True,
    }.items():
        if getattr(user, field) != value:
            setattr(user, field, value)
            dirty = True
    if password:
        user.set_password(password)
        dirty = True
    elif created:
        user.set_unusable_password()
        dirty = True
    if dirty:
        user.save()
    return user, created


def ensure_checkin(user, place_name, place_address, when, location, symptoms=None):
    symptoms = symptoms or {}
    defaults = {
        "place_address": place_address,
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "geo": location["geo"],
        "province": location["province"],
        "amphur": location["amphur"],
        "district": location["district"],
        "sick1": symptoms.get("sick1", 0),
        "sick2": symptoms.get("sick2", 0),
        "sick3": symptoms.get("sick3", 0),
        "sick4": symptoms.get("sick4", 0),
        "sick5": symptoms.get("sick5", 0),
        "sick6": symptoms.get("sick6", 0),
        "sick7": symptoms.get("sick7", 1),
    }
    item = gps.objects.filter(user=user, place_name=place_name, created_at=when).first()
    created = item is None
    if created:
        item = gps.objects.create(user=user, place_name=place_name, **defaults)
    else:
        for field, value in defaults.items():
            setattr(item, field, value)
        item.save()

    gps.objects.filter(pk=item.pk).update(created_at=when, updated_at=when)
    item.refresh_from_db()
    return item, created


def ensure_user_dorm(user, dorm):
    item = UserDorm.objects.filter(user=user, dorm=dorm).first()
    if item:
        return item, False
    return UserDorm.objects.create(user=user, dorm=dorm), True


def ensure_profile(user, location, **values):
    defaults = {
        "address": values.get("address", "99 หมู่ 2 ต.แม่กา อ.เมืองพะเยา จ.พะเยา"),
        "geo": location["geo"],
        "province": location["province"],
        "amphur": location["amphur"],
        "district": location["district"],
        "post": values.get("post", "56000"),
        "tel": values.get("tel", "0800000000"),
        "faculty": values.get("faculty", "คณะเทคโนโลยีสารสนเทศและการสื่อสาร"),
        "question1": values.get("question1", 0),
        "question2": values.get("question2", 0),
        "question3": values.get("question3", 0),
        "address2": values.get("address2", "หอพักแม่กา กรีนเพลส"),
    }
    item, created = profile.objects.update_or_create(user=user, defaults=defaults)
    return item, created


def ensure_choice(name, value):
    return Choice.objects.get_or_create(name=name, value=value)


def ensure_dorm_detail(dorm):
    return DormDetail.objects.update_or_create(
        dorm=dorm,
        defaults={
            "build": 2,
            "floor": 4,
            "room": 96,
            "all_count": 180,
            "now_count": 142,
            "width": 4,
            "height": 6,
            "fan_price_month": 2800,
            "fan_price_day": 350,
            "air_price_month": 3800,
            "air_price_day": 500,
            "electric_unit": 8,
            "water_unit": 20,
            "water_month": "ต่อคน",
            "water_internet": 250,
        },
    )


def ensure_dorm_owner(dorm):
    item = DormOwner.objects.filter(dorm=dorm, name="คุณพิมพ์ใจ แม่กา").first()
    if item:
        if item.type_owner != "เจ้าของหอพักดูแลเอง":
            item.type_owner = "เจ้าของหอพักดูแลเอง"
            item.save(update_fields=["type_owner"])
        return item, False
    return DormOwner.objects.create(
        dorm=dorm,
        name="คุณพิมพ์ใจ แม่กา",
        type_owner="เจ้าของหอพักดูแลเอง",
    ), True


def ensure_dorm_image(dorm):
    item = DormImage.objects.filter(dorm=dorm).first()
    if item:
        return item, False
    return DormImage.objects.create(dorm=dorm), True


def ensure_dorm_styles(dorm):
    specs = [
        ("โซนหอพัก", "A"),
        ("ประเภทของหอพัก", "หอพักเอกชน"),
        ("ลักษณะของหอพัก", "ห้องแอร์"),
        ("ลักษณะการเข้าพักอาศัย", "พักคู่"),
        ("สิ่งอำนวยความสะดวกภายในหอพัก ", "อินเทอร์เน็ต"),
        ("ระบบรักษาความปลอดภัย", "คีย์การ์ดและกล้องวงจรปิด"),
        ("ทำอาหารในหอพักได้หรือไม่", "ทำอาหารได้"),
        ("เลี้ยงสัตว์เลี้ยงในหอพักได้หรือไม่", "ไม่อนุญาต"),
        ("การเผยแพร่ข้อมูลหอพัก", "เผยแพร่"),
        ("ราคาหอพัก", "3,000-4,000 บาท"),
    ]
    created_count = 0
    for name, value in specs:
        choice, choice_created = ensure_choice(name, value)
        _, style_created = DormStyle.objects.get_or_create(dorm=dorm, choice=choice, defaults={"other": ""})
        created_count += int(choice_created) + int(style_created)
    return created_count


def ensure_about_demo():
    item, created = About.objects.update_or_create(
        title="UP Checkin Demo",
        defaults={
            "text": "ข้อมูลตัวอย่างสำหรับทดลองระบบเช็คอิน หอพัก เหรียญ และ timeline",
            "beta": True,
            "body": "ชุดข้อมูลนี้สร้างจาก command seed_demo_data สำหรับการสาธิตในเครื่อง local",
        },
    )
    return item, created


def set_model_timestamp(model, pk, when):
    model.objects.filter(pk=pk).update(created_at=when, updated_at=when)


def set_created_timestamp(model, pk, when):
    model.objects.filter(pk=pk).update(created_at=when)


def ensure_legacy_point(user):
    item, created = point.objects.update_or_create(
        user=user,
        defaults={
            "points": 40,
            "points2": 30,
            "points3": 20,
            "points4": 10,
            "points5": 5,
            "points6": 0,
            "points7": 105,
            "status": 1,
        },
    )
    return item, created


def phayao_demo_location():
    geo, _ = first_or_create(Geography, {"name": "ภาคเหนือ"})
    province, _ = first_or_create(
        Province,
        {"code": "56"},
        {"name": "พะเยา", "geo": geo},
    )
    if province.name != "พะเยา" or province.geo_id != geo.id:
        province.name = "พะเยา"
        province.geo = geo
        province.save()

    amphur, _ = first_or_create(
        Amphur,
        {"code": "5601"},
        {"name": "เมืองพะเยา", "geo": geo, "province": province},
    )
    if amphur.name != "เมืองพะเยา" or amphur.geo_id != geo.id or amphur.province_id != province.id:
        amphur.name = "เมืองพะเยา"
        amphur.geo = geo
        amphur.province = province
        amphur.save()

    district, _ = first_or_create(
        District,
        {"code": "560116"},
        {"name": "แม่กา", "geo": geo, "province": province, "amphur": amphur},
    )
    if (
        district.name != "แม่กา"
        or district.geo_id != geo.id
        or district.province_id != province.id
        or district.amphur_id != amphur.id
    ):
        district.name = "แม่กา"
        district.geo = geo
        district.province = province
        district.amphur = amphur
        district.save()

    return {
        "geo": geo,
        "province": province,
        "amphur": amphur,
        "district": district,
        "latitude": "19.030000",
        "longitude": "99.895000",
    }


def ensure_demo_dorm(location):
    dorm, created = first_or_create(
        Dorm,
        {"name": "หอพักแม่กา กรีนเพลส"},
        {
            "address": "99 หมู่ 2 ต.แม่กา อ.เมืองพะเยา จ.พะเยา ใกล้มหาวิทยาลัยพะเยา",
            "geo": location["geo"],
            "province": location["province"],
            "amphur": location["amphur"],
            "district": location["district"],
            "post": "56000",
            "tel": "054000001",
            "latitude": "19.029700",
            "longitude": "99.894600",
            "permission": True,
            "advt": True,
        },
    )
    for field, value in {
        "address": "99 หมู่ 2 ต.แม่กา อ.เมืองพะเยา จ.พะเยา ใกล้มหาวิทยาลัยพะเยา",
        "geo": location["geo"],
        "province": location["province"],
        "amphur": location["amphur"],
        "district": location["district"],
        "post": "56000",
        "tel": "054000001",
        "latitude": "19.029700",
        "longitude": "99.894600",
        "permission": True,
        "advt": True,
    }.items():
        if getattr(dorm, field) != value:
            setattr(dorm, field, value)
    dorm.save()
    return dorm, created


def ensure_secondary_demo_dorm(location):
    dorm, created = first_or_create(
        Dorm,
        {"name": "หอพักกว๊านพะเยา เพลส"},
        {
            "address": "ถนนพหลโยธิน ต.แม่กา อ.เมืองพะเยา จ.พะเยา",
            "geo": location["geo"],
            "province": location["province"],
            "amphur": location["amphur"],
            "district": location["district"],
            "post": "56000",
            "tel": "054000002",
            "latitude": "19.036300",
            "longitude": "99.891000",
            "permission": True,
            "advt": True,
        },
    )
    return dorm, created


def demo_checkin_specs():
    return [
        ("หอพักแม่กา กรีนเพลส", "99 หมู่ 2 ต.แม่กา อ.เมืองพะเยา จ.พะเยา", (2026, 4, 20, 7, 45), "19.029700", "99.894600", {"sick7": 1}),
        ("โรงอาหารกลาง มหาวิทยาลัยพะเยา", "มหาวิทยาลัยพะเยา ต.แม่กา อ.เมืองพะเยา", (2026, 4, 21, 12, 5), "19.028600", "99.895900", {"sick7": 1}),
        ("อาคารเรียนรวม CE", "มหาวิทยาลัยพะเยา ต.แม่กา อ.เมืองพะเยา", (2026, 4, 22, 9, 10), "19.031200", "99.897500", {"sick7": 1}),
        ("ห้องสมุด มหาวิทยาลัยพะเยา", "มหาวิทยาลัยพะเยา ต.แม่กา อ.เมืองพะเยา", (2026, 4, 23, 15, 40), "19.030800", "99.898400", {"sick7": 1}),
        ("ลานกิจกรรมนิสิต", "มหาวิทยาลัยพะเยา ต.แม่กา อ.เมืองพะเยา", (2026, 4, 24, 17, 20), "19.032000", "99.896700", {"sick7": 1}),
        ("หอพักแม่กา กรีนเพลส", "99 หมู่ 2 ต.แม่กา อ.เมืองพะเยา จ.พะเยา", (2026, 4, 25, 8, 0), "19.029700", "99.894600", {"sick7": 1}),
        ("ตลาดแม่กา", "ต.แม่กา อ.เมืองพะเยา จ.พะเยา", (2026, 4, 26, 18, 20), "19.036500", "99.891200", {"sick7": 1}),
        ("ร้านกาแฟหน้ามอ", "ต.แม่กา อ.เมืองพะเยา จ.พะเยา", (2026, 4, 27, 10, 30), "19.039500", "99.887000", {"sick7": 1}),
        ("อาคาร ICT", "มหาวิทยาลัยพะเยา ต.แม่กา อ.เมืองพะเยา", (2026, 4, 28, 13, 20), "19.032500", "99.897800", {"sick7": 1}),
        ("สนามกีฬากลาง", "มหาวิทยาลัยพะเยา ต.แม่กา อ.เมืองพะเยา", (2026, 4, 29, 16, 45), "19.033700", "99.900100", {"sick7": 1}),
        ("หอพักแม่กา กรีนเพลส", "99 หมู่ 2 ต.แม่กา อ.เมืองพะเยา จ.พะเยา", (2026, 4, 30, 8, 5), "19.029700", "99.894600", {"sick7": 1}),
        ("โรงอาหารกลาง มหาวิทยาลัยพะเยา", "มหาวิทยาลัยพะเยา ต.แม่กา อ.เมืองพะเยา", (2026, 5, 1, 12, 10), "19.028600", "99.895900", {"sick1": 1, "sick7": 0}),
        ("อาคารเรียนรวม CE", "มหาวิทยาลัยพะเยา ต.แม่กา อ.เมืองพะเยา", (2026, 5, 2, 9, 15), "19.031200", "99.897500", {"sick2": 1, "sick7": 0}),
        ("ห้องสมุด มหาวิทยาลัยพะเยา", "มหาวิทยาลัยพะเยา ต.แม่กา อ.เมืองพะเยา", (2026, 5, 3, 15, 30), "19.030800", "99.898400", {"sick7": 1}),
        ("ตลาดแม่กา", "ต.แม่กา อ.เมืองพะเยา จ.พะเยา", (2026, 5, 4, 18, 10), "19.036500", "99.891200", {"sick7": 1}),
        ("โรงพยาบาลมหาวิทยาลัยพะเยา", "มหาวิทยาลัยพะเยา ต.แม่กา อ.เมืองพะเยา", (2026, 5, 5, 10, 20), "19.027900", "99.899300", {"sick3": 1, "sick7": 0}),
        ("หอพักแม่กา กรีนเพลส", "99 หมู่ 2 ต.แม่กา อ.เมืองพะเยา จ.พะเยา", (2026, 5, 6, 8, 0), "19.029700", "99.894600", {"sick7": 1}),
        ("อาคาร ICT", "มหาวิทยาลัยพะเยา ต.แม่กา อ.เมืองพะเยา", (2026, 5, 7, 13, 0), "19.032500", "99.897800", {"sick7": 1}),
        ("ร้านกาแฟหน้ามอ", "ต.แม่กา อ.เมืองพะเยา จ.พะเยา", (2026, 5, 8, 11, 25), "19.039500", "99.887000", {"sick7": 1}),
        ("หอพักแม่กา กรีนเพลส", "99 หมู่ 2 ต.แม่กา อ.เมืองพะเยา จ.พะเยา", (2026, 5, 9, 8, 15), "19.029700", "99.894600", {"sick7": 1}),
    ]


def ensure_demo_checkins(user, location):
    checkins = []
    for place_name, place_address, when_args, latitude, longitude, symptoms in demo_checkin_specs():
        item_location = dict(location)
        item_location.update({"latitude": latitude, "longitude": longitude})
        item, _ = ensure_checkin(
            user,
            place_name,
            place_address,
            aware_datetime(*when_args),
            item_location,
            symptoms=symptoms,
        )
        checkins.append(item)
    return checkins


def ensure_demo_contacts(users, location):
    contact_specs = [
        ("demo_contact_high", "โรงอาหารกลาง มหาวิทยาลัยพะเยา", "มหาวิทยาลัยพะเยา ต.แม่กา อ.เมืองพะเยา", (2026, 5, 1, 13, 20), "19.028650", "99.895920"),
        ("demo_contact_medium", "ห้องสมุด มหาวิทยาลัยพะเยา", "มหาวิทยาลัยพะเยา ต.แม่กา อ.เมืองพะเยา", (2026, 5, 3, 21, 45), "19.030850", "99.898450"),
        ("demo_contact_low", "ร้านกาแฟหน้ามอ", "ต.แม่กา อ.เมืองพะเยา จ.พะเยา", (2026, 5, 2, 10, 5), "19.039500", "99.887000"),
    ]
    checkins = []
    for username, place_name, place_address, when_args, latitude, longitude in contact_specs:
        item_location = dict(location)
        item_location.update({"latitude": latitude, "longitude": longitude})
        item, _ = ensure_checkin(
            users[username],
            place_name,
            place_address,
            aware_datetime(*when_args),
            item_location,
            symptoms={"sick7": 1},
        )
        checkins.append(item)
    return checkins


def reset_demo_coin_data(user):
    user_cut_coin.objects.filter(user=user).delete()
    CoinTransaction.objects.filter(user=user).delete()
    wallet = get_coin_wallet(user)
    wallet.balance = 0
    wallet.current_streak = 0
    wallet.longest_streak = 0
    wallet.last_checkin_date = None
    wallet.total_earned = 0
    wallet.total_spent = 0
    wallet.activity_hours = Decimal("0")
    wallet.save()


@transaction.atomic
def seed_demo_data():
    stats = Counter()
    location = phayao_demo_location()
    rewards = ensure_default_activity_rewards()
    stats["rewards"] = len(rewards)

    dorm, created = ensure_demo_dorm(location)
    stats["dorms_created"] += int(created)
    secondary_dorm, created = ensure_secondary_demo_dorm(location)
    stats["dorms_created"] += int(created)
    ensure_dorm_detail(dorm)
    ensure_dorm_owner(dorm)
    ensure_dorm_image(dorm)
    stats["dorm_styles_created"] += ensure_dorm_styles(dorm)
    ensure_about_demo()

    user_specs = [
        ("demo_admin", "Demo", "Admin", "demo_admin@example.test", True, True, DEMO_PASSWORD),
        ("demo_user", "Demo", "User", "demo_user@example.test", False, False, DEMO_PASSWORD),
        ("demo_contact_high", "มาลี", "ใกล้ชิด", "demo_contact_high@example.test", False, False, None),
        ("demo_contact_medium", "กานต์", "ร่วมพื้นที่", "demo_contact_medium@example.test", False, False, None),
        ("demo_contact_low", "ปรีชา", "ผ่านพื้นที่", "demo_contact_low@example.test", False, False, None),
        ("demo_contact_dorm", "อร", "ร่วมหอ", "demo_contact_dorm@example.test", False, False, None),
    ]
    users = {}
    for username, first_name, last_name, email, is_staff, is_superuser, password in user_specs:
        users[username], created = ensure_mock_user(
            username,
            first_name,
            last_name,
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,
            password=password,
        )
        stats["users_created"] += int(created)

    ensure_profile(
        users["demo_user"],
        location,
        tel="0812345678",
        faculty="คณะเทคโนโลยีสารสนเทศและการสื่อสาร",
        address2=dorm.name,
    )
    ensure_profile(
        users["demo_admin"],
        location,
        tel="0890000001",
        faculty="ศูนย์บริหารจัดการความปลอดภัย",
        address="อาคารสำนักงานมหาวิทยาลัยพะเยา ต.แม่กา อ.เมืองพะเยา จ.พะเยา",
        address2="สำนักงานเจ้าหน้าที่",
    )
    for username in ("demo_contact_high", "demo_contact_medium", "demo_contact_low", "demo_contact_dorm"):
        ensure_profile(users[username], location, tel="0800000000", address2=secondary_dorm.name)

    for username in ("demo_user", "demo_contact_dorm"):
        _, created = ensure_user_dorm(users[username], dorm)
        stats["user_dorms_created"] += int(created)

    checkins = ensure_demo_checkins(users["demo_user"], location)
    contact_checkins = ensure_demo_contacts(users, location)
    ensure_legacy_point(users["demo_user"])

    reset_demo_coin_data(users["demo_user"])
    wallet = rebuild_checkin_rewards_for_user(users["demo_user"])
    redeem_reward = next((reward for reward in rewards if int(reward.coin or 0) == 180), rewards[0])
    redemption = redeem_activity_reward(users["demo_user"], redeem_reward)
    set_created_timestamp(user_cut_coin, redemption.pk, aware_datetime(2026, 5, 9, 12, 0))
    wallet.refresh_from_db()

    covid_case = CovidCase.objects.filter(
        user=users["demo_user"],
        notes__contains=DEMO_MOCK_TAG,
    ).first()
    case_defaults = {
        "status": CovidCase.STATUS_CONFIRMED,
        "symptom_started_on": date(2026, 5, 1),
        "confirmed_on": date(2026, 5, 5),
        "trace_start_date": date(2026, 5, 1),
        "trace_end_date": date(2026, 5, 5),
        "created_by": users["demo_admin"],
        "notes": "%s เคส demo_user สำหรับสาธิต timeline, contact, export CSV และข้อมูลหอพัก" % DEMO_MOCK_TAG,
    }
    if covid_case is None:
        covid_case = CovidCase.objects.create(user=users["demo_user"], **case_defaults)
        stats["cases_created"] += 1
    else:
        for field, value in case_defaults.items():
            setattr(covid_case, field, value)
        covid_case.save()
        stats["cases_updated"] += 1

    stats["checkins"] = len(checkins)
    stats["contact_checkins"] = len(contact_checkins)
    stats["wallet_balance"] = wallet.balance
    stats["wallet_total_earned"] = wallet.total_earned
    stats["wallet_total_spent"] = wallet.total_spent

    return {
        "admin": users["demo_admin"],
        "user": users["demo_user"],
        "contacts": {
            "high": users["demo_contact_high"],
            "medium": users["demo_contact_medium"],
            "low": users["demo_contact_low"],
            "dorm": users["demo_contact_dorm"],
        },
        "case": covid_case,
        "wallet": wallet,
        "dorm": dorm,
        "checkins": checkins,
        "contact_checkins": contact_checkins,
        "stats": stats,
    }


@transaction.atomic
def seed_timeline_mock_data():
    stats = Counter()

    geo, created = first_or_create(Geography, {"name": "ภาคเหนือ"})
    stats["created"] += int(created)

    province, created = first_or_create(
        Province,
        {"code": "56"},
        {"name": "พะเยา", "geo": geo},
    )
    if province.name != "พะเยา" or province.geo_id != geo.id:
        province.name = "พะเยา"
        province.geo = geo
        province.save()
        stats["updated"] += 1
    stats["created"] += int(created)

    amphur, created = first_or_create(
        Amphur,
        {"code": "5601"},
        {"name": "เมืองพะเยา", "geo": geo, "province": province},
    )
    if amphur.name != "เมืองพะเยา" or amphur.geo_id != geo.id or amphur.province_id != province.id:
        amphur.name = "เมืองพะเยา"
        amphur.geo = geo
        amphur.province = province
        amphur.save()
        stats["updated"] += 1
    stats["created"] += int(created)

    district, created = first_or_create(
        District,
        {"code": "560116"},
        {"name": "แม่กา", "geo": geo, "province": province, "amphur": amphur},
    )
    if (
        district.name != "แม่กา"
        or district.geo_id != geo.id
        or district.province_id != province.id
        or district.amphur_id != amphur.id
    ):
        district.name = "แม่กา"
        district.geo = geo
        district.province = province
        district.amphur = amphur
        district.save()
        stats["updated"] += 1
    stats["created"] += int(created)

    location = {
        "geo": geo,
        "province": province,
        "amphur": amphur,
        "district": district,
        "latitude": "19.030000",
        "longitude": "99.895000",
    }

    dorm, created = first_or_create(
        Dorm,
        {"name": "หอพักแม่กา กรีนเพลส"},
        {
            "address": "ต.แม่กา อ.เมืองพะเยา จ.พะเยา ใกล้มหาวิทยาลัยพะเยา",
            "geo": geo,
            "province": province,
            "amphur": amphur,
            "district": district,
            "post": "56000",
            "tel": "054000001",
            "latitude": "19.029700",
            "longitude": "99.894600",
            "permission": True,
            "advt": True,
        },
    )
    for field, value in {
        "address": "ต.แม่กา อ.เมืองพะเยา จ.พะเยา ใกล้มหาวิทยาลัยพะเยา",
        "geo": geo,
        "province": province,
        "amphur": amphur,
        "district": district,
        "post": "56000",
        "tel": "054000001",
        "latitude": "19.029700",
        "longitude": "99.894600",
        "permission": True,
        "advt": True,
    }.items():
        if getattr(dorm, field) != value:
            setattr(dorm, field, value)
    dorm.save()
    stats["created"] += int(created)

    user_specs = [
        ("timeline_staff", "เจ้าหน้าที่", "Timeline", "timeline_staff@example.test", True),
        ("timeline_case_01", "นที", "ใจดี", "timeline_case_01@example.test", False),
        ("timeline_contact_high", "มาลี", "ใกล้ชิด", "timeline_contact_high@example.test", False),
        ("timeline_contact_medium", "กานต์", "ร่วมพื้นที่", "timeline_contact_medium@example.test", False),
        ("timeline_contact_low", "ปรีชา", "ผ่านพื้นที่", "timeline_contact_low@example.test", False),
        ("timeline_contact_dorm", "อร", "ร่วมหอ", "timeline_contact_dorm@example.test", False),
    ]
    users = {}
    for username, first_name, last_name, email, is_staff in user_specs:
        users[username], created = ensure_mock_user(
            username,
            first_name,
            last_name,
            email=email,
            is_staff=is_staff,
        )
        stats["users_created"] += int(created)

    for username in ("timeline_case_01", "timeline_contact_dorm"):
        _, created = ensure_user_dorm(users[username], dorm)
        stats["user_dorms_created"] += int(created)

    checkin_specs = [
        (
            "timeline_case_01",
            "หอพักแม่กา กรีนเพลส",
            "ต.แม่กา อ.เมืองพะเยา จ.พะเยา",
            aware_datetime(2026, 5, 1, 8, 30),
            {"latitude": "19.029700", "longitude": "99.894600"},
            {"sick7": 1},
        ),
        (
            "timeline_case_01",
            "โรงอาหารกลาง มหาวิทยาลัยพะเยา",
            "มหาวิทยาลัยพะเยา ต.แม่กา อ.เมืองพะเยา",
            aware_datetime(2026, 5, 1, 12, 10),
            {"latitude": "19.028600", "longitude": "99.895900"},
            {"sick1": 1, "sick7": 0},
        ),
        (
            "timeline_case_01",
            "อาคารเรียนรวม CE",
            "มหาวิทยาลัยพะเยา ต.แม่กา อ.เมืองพะเยา",
            aware_datetime(2026, 5, 2, 9, 15),
            {"latitude": "19.031200", "longitude": "99.897500"},
            {"sick2": 1, "sick7": 0},
        ),
        (
            "timeline_case_01",
            "ห้องสมุด มหาวิทยาลัยพะเยา",
            "มหาวิทยาลัยพะเยา ต.แม่กา อ.เมืองพะเยา",
            aware_datetime(2026, 5, 3, 15, 30),
            {"latitude": "19.030800", "longitude": "99.898400"},
            {"sick7": 1},
        ),
        (
            "timeline_case_01",
            "ตลาดแม่กา",
            "ต.แม่กา อ.เมืองพะเยา จ.พะเยา",
            aware_datetime(2026, 5, 4, 18, 10),
            {"latitude": "19.036500", "longitude": "99.891200"},
            {"sick7": 1},
        ),
        (
            "timeline_case_01",
            "โรงพยาบาลมหาวิทยาลัยพะเยา",
            "มหาวิทยาลัยพะเยา ต.แม่กา อ.เมืองพะเยา",
            aware_datetime(2026, 5, 5, 10, 20),
            {"latitude": "19.027900", "longitude": "99.899300"},
            {"sick3": 1, "sick7": 0},
        ),
        (
            "timeline_contact_high",
            "โรงอาหารกลาง มหาวิทยาลัยพะเยา",
            "มหาวิทยาลัยพะเยา ต.แม่กา อ.เมืองพะเยา",
            aware_datetime(2026, 5, 1, 13, 20),
            {"latitude": "19.028650", "longitude": "99.895920"},
            {"sick7": 1},
        ),
        (
            "timeline_contact_medium",
            "ห้องสมุด มหาวิทยาลัยพะเยา",
            "มหาวิทยาลัยพะเยา ต.แม่กา อ.เมืองพะเยา",
            aware_datetime(2026, 5, 3, 21, 45),
            {"latitude": "19.030850", "longitude": "99.898450"},
            {"sick7": 1},
        ),
        (
            "timeline_contact_low",
            "ร้านกาแฟหน้ามอ",
            "ต.แม่กา อ.เมืองพะเยา จ.พะเยา",
            aware_datetime(2026, 5, 2, 10, 5),
            {"latitude": "19.039500", "longitude": "99.887000"},
            {"sick7": 1},
        ),
    ]

    checkins = []
    for username, place_name, place_address, when, coordinates, symptoms in checkin_specs:
        item_location = dict(location)
        item_location.update(coordinates)
        item, created = ensure_checkin(
            users[username],
            place_name,
            place_address,
            when,
            item_location,
            symptoms=symptoms,
        )
        checkins.append(item)
        stats["checkins_created"] += int(created)
        stats["checkins_updated"] += int(not created)

    covid_case = CovidCase.objects.filter(
        user=users["timeline_case_01"],
        notes__contains=TIMELINE_MOCK_TAG,
    ).first()
    case_defaults = {
        "status": CovidCase.STATUS_CONFIRMED,
        "symptom_started_on": date(2026, 5, 1),
        "confirmed_on": date(2026, 5, 5),
        "trace_start_date": date(2026, 5, 1),
        "trace_end_date": date(2026, 5, 5),
        "created_by": users["timeline_staff"],
        "notes": "%s เคสตัวอย่างสำหรับทดสอบ timeline และ contact tracing" % TIMELINE_MOCK_TAG,
    }
    if covid_case is None:
        covid_case = CovidCase.objects.create(user=users["timeline_case_01"], **case_defaults)
        stats["cases_created"] += 1
    else:
        for field, value in case_defaults.items():
            setattr(covid_case, field, value)
        covid_case.save()
        stats["cases_updated"] += 1

    return {
        "case": covid_case,
        "checkins": checkins,
        "users": users,
        "dorm": dorm,
        "stats": stats,
    }
