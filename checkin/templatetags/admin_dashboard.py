from datetime import timedelta

from django import template
from django.apps import apps
from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import NoReverseMatch, reverse
from django.utils import timezone

from checkin.models.checkin import CoinWallet, CovidCase, gps, user_cut_coin
from checkin.services import get_day_bounds
from dormitory.models import Dorm, UserDorm


register = template.Library()


def admin_url(name):
    try:
        return reverse(name)
    except NoReverseMatch:
        return ""


@register.filter
def compact_number(value):
    try:
        number = int(value or 0)
    except (TypeError, ValueError):
        return value
    if abs(number) >= 1_000_000:
        return "%.1fm" % (number / 1_000_000)
    if abs(number) >= 1_000:
        return "%.1fk" % (number / 1_000)
    return str(number)


@register.simple_tag
def model_object_count(app_label, object_name):
    try:
        model = apps.get_model(app_label, object_name)
    except LookupError:
        return 0
    return model._default_manager.count()


@register.simple_tag
def model_icon(object_name):
    icons = {
        "user": "US",
        "group": "GR",
        "gps": "CI",
        "covidcase": "TL",
        "coinwallet": "CW",
        "cointransaction": "TX",
        "cut_coin": "RW",
        "user_cut_coin": "RD",
        "profile": "PF",
        "province": "PV",
        "amphur": "AM",
        "district": "DT",
        "geography": "GE",
        "dorm": "DM",
        "userdorm": "UD",
        "choice": "CH",
        "dormdetail": "DD",
        "dormowner": "DO",
        "dormstyle": "DS",
        "dormimage": "DI",
        "about": "AB",
    }
    return icons.get((object_name or "").lower(), "DB")


@register.simple_tag
def admin_dashboard_metrics():
    today = timezone.localdate()
    start_at, end_at = get_day_bounds(today)
    total_balance = CoinWallet.objects.aggregate(total=Sum("balance"))["total"] or 0
    confirmed_cases = CovidCase.objects.filter(status=CovidCase.STATUS_CONFIRMED).count()
    active_cases = CovidCase.objects.exclude(status=CovidCase.STATUS_CLEARED).count()

    return [
        {
            "label": "Check-ins วันนี้",
            "value": gps.objects.filter(created_at__gte=start_at, created_at__lt=end_at).count(),
            "meta": "รายการเช็คอินล่าสุด",
            "url": admin_url("admin:checkin_gps_changelist"),
            "tone": "rose",
            "icon": "CI",
        },
        {
            "label": "ผู้ใช้ทั้งหมด",
            "value": User.objects.count(),
            "meta": "%s active accounts" % User.objects.filter(is_active=True).count(),
            "url": admin_url("admin:auth_user_changelist"),
            "tone": "teal",
            "icon": "US",
        },
        {
            "label": "เคส COVID",
            "value": CovidCase.objects.count(),
            "meta": "%s confirmed / %s active" % (confirmed_cases, active_cases),
            "url": admin_url("admin:checkin_covidcase_changelist"),
            "tone": "indigo",
            "icon": "TL",
        },
        {
            "label": "เหรียญในระบบ",
            "value": total_balance,
            "meta": "%s รายการแลก" % user_cut_coin.objects.count(),
            "url": admin_url("admin:checkin_coinwallet_changelist"),
            "tone": "amber",
            "icon": "CW",
        },
    ]


@register.simple_tag
def admin_dashboard_chart(days=7):
    today = timezone.localdate()
    items = []
    for offset in range(days - 1, -1, -1):
        day = today - timedelta(days=offset)
        start_at, end_at = get_day_bounds(day)
        value = gps.objects.filter(created_at__gte=start_at, created_at__lt=end_at).count()
        items.append({"label": day.strftime("%d/%m"), "value": value})

    maximum = max([item["value"] for item in items] + [1])
    for item in items:
        item["height"] = max(10, int((item["value"] / maximum) * 100))
    return items


@register.simple_tag
def recent_checkins(limit=5):
    return (
        gps.objects.select_related("user", "province", "amphur", "district")
        .order_by("-created_at", "-id")[:limit]
    )


@register.simple_tag
def recent_cases(limit=4):
    return (
        CovidCase.objects.select_related("user", "created_by")
        .order_by("-updated_at", "-created_at")[:limit]
    )


@register.simple_tag
def recent_admin_actions(limit=6):
    return LogEntry.objects.select_related("content_type", "user").order_by("-action_time")[:limit]


@register.simple_tag
def admin_dashboard_counts():
    return {
        "dorms": Dorm.objects.count(),
        "user_dorms": UserDorm.objects.count(),
        "redemptions": user_cut_coin.objects.count(),
        "wallets": CoinWallet.objects.count(),
    }
