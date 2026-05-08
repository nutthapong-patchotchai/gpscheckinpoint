from math import asin, cos, radians, sin, sqrt
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from checkin.forms import CheckinForm, LocalUserCreationForm
from checkin.models.checkin import CoinTransaction, cut_coin, gps, user_cut_coin
from checkin.models.user import profile
from checkin.services import (
    CoinError,
    InsufficientCoins,
    award_daily_checkin_coins,
    get_coin_wallet,
    redeem_activity_reward,
)
from dormitory.models import Dorm, UserDorm


PHAYAO_MAP_BOUNDS = {
    "min_lat": 18.75,
    "max_lat": 19.80,
    "min_lng": 99.55,
    "max_lng": 100.55,
}

 
def register(request):
    if request.user.is_authenticated:
        return redirect("home")

    form = LocalUserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "สมัครสมาชิกเรียบร้อยแล้ว เริ่มใช้งานได้ทันที")
        return redirect("home")

    return render(request, "registration/register.html", {"form": form})


@login_required
def home(request):
    form = CheckinForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        checkin = form.save(request.user)
        award = award_daily_checkin_coins(checkin)
        if award.awarded:
            messages.success(
                request,
                "บันทึกการเช็คอินเรียบร้อยแล้ว ได้รับ %s เหรียญ (เช็คอินต่อเนื่อง %s วัน)"
                % (award.amount, award.streak_day),
            )
        else:
            messages.success(
                request,
                "บันทึกการเช็คอินเรียบร้อยแล้ว วันนี้รับเหรียญจากการเช็คอินไปแล้ว",
            )
        return redirect("checkin_history")

    wallet = get_coin_wallet(request.user)
    latest_checkins = (
        gps.objects.filter(user=request.user)
        .select_related("geo", "province", "amphur", "district")
        .order_by("-created_at")[:5]
    )
    return render(
        request,
        "checkin/home.html",
        {
            "form": form,
            "wallet": wallet,
            "latest_checkins": latest_checkins,
        },
    )


def distance_km(lat1, lng1, lat2, lng2):
    radius = 6371
    dlat = radians(lat2 - lat1)
    dlng = radians(lng2 - lng1)
    a = (
        sin(dlat / 2) ** 2
        + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlng / 2) ** 2
    )
    return 2 * radius * asin(sqrt(a))


def clamp(value, minimum, maximum):
    return max(minimum, min(value, maximum))


def build_map_point(item):
    try:
        latitude = float(item.latitude)
        longitude = float(item.longitude)
    except (TypeError, ValueError):
        return None

    x = ((longitude - PHAYAO_MAP_BOUNDS["min_lng"]) / (
        PHAYAO_MAP_BOUNDS["max_lng"] - PHAYAO_MAP_BOUNDS["min_lng"]
    )) * 100
    y = 100 - ((latitude - PHAYAO_MAP_BOUNDS["min_lat"]) / (
        PHAYAO_MAP_BOUNDS["max_lat"] - PHAYAO_MAP_BOUNDS["min_lat"]
    )) * 100
    x = clamp(x, 4, 96)
    y = clamp(y, 4, 96)
    has_symptom = any([
        item.sick1,
        item.sick2,
        item.sick3,
        item.sick4,
        item.sick5,
        item.sick6,
    ])
    return {
        "id": item.id,
        "x": f"{x:.2f}",
        "y": f"{y:.2f}",
        "svg_x": f"{x:.2f}",
        "svg_y": f"{y:.2f}",
        "place_name": item.location_label,
        "place_address": item.place_address,
        "district": item.district.name if item.district else "-",
        "amphur": item.amphur.name if item.amphur else "-",
        "province": item.province.name if item.province else "-",
        "created_at": item.created_at,
        "has_symptom": has_symptom,
    }


@login_required
def resolve_location(request):
    try:
        latitude = float(request.GET.get("lat", ""))
        longitude = float(request.GET.get("lng", ""))
    except ValueError:
        return JsonResponse({"detail": "พิกัดไม่ถูกต้อง"}, status=400)

    nearest = None
    nearest_distance = None
    dorms = Dorm.objects.select_related("geo", "province", "amphur", "district").filter(
        latitude__isnull=False,
        longitude__isnull=False,
    )
    for dorm in dorms:
        try:
            dorm_latitude = float(dorm.latitude)
            dorm_longitude = float(dorm.longitude)
        except (TypeError, ValueError):
            continue

        distance = distance_km(latitude, longitude, dorm_latitude, dorm_longitude)
        if nearest is None or distance < nearest_distance:
            nearest = dorm
            nearest_distance = distance

    if nearest is None:
        return JsonResponse(
            {
                "detail": "ยังไม่มีข้อมูลสถานที่ในระบบสำหรับเทียบพิกัด",
                "latitude": latitude,
                "longitude": longitude,
            },
            status=404,
        )

    return JsonResponse(
        {
            "place_name": nearest.name,
            "address": nearest.address,
            "distance_km": round(nearest_distance or 0, 2),
            "geo": {"id": nearest.geo_id, "name": nearest.geo.name},
            "province": {"id": nearest.province_id, "name": nearest.province.name},
            "amphur": {"id": nearest.amphur_id, "name": nearest.amphur.name},
            "district": {"id": nearest.district_id, "name": nearest.district.name},
        }
    )


@login_required
def history(request):
    since = timezone.now() - timedelta(days=14)
    checkins = (
        gps.objects.filter(user=request.user)
        .select_related("geo", "province", "amphur", "district")
        .order_by("-created_at")
    )
    recent_checkins = checkins.filter(created_at__gte=since).order_by("created_at")
    map_points = [
        point
        for point in (build_map_point(item) for item in recent_checkins)
        if point is not None
    ]
    map_path_points = " ".join(
        f"{point['svg_x']},{point['svg_y']}"
        for point in map_points
    )
    user_profile = (
        profile.objects.filter(user=request.user)
        .select_related("geo", "province", "amphur", "district")
        .first()
    )
    current_dorm = (
        UserDorm.objects.filter(user=request.user)
        .select_related("dorm", "dorm__province", "dorm__amphur", "dorm__district")
        .order_by("-created_at")
        .first()
    )
    return render(
        request,
        "checkin/history.html",
        {
            "checkins": checkins,
            "user_profile": user_profile,
            "current_dorm": current_dorm,
            "wallet": get_coin_wallet(request.user),
            "map_points": map_points,
            "map_path_points": map_path_points,
            "map_since": since,
        },
    )


@login_required
def coins(request):
    wallet = get_coin_wallet(request.user)

    if request.method == "POST":
        reward = get_object_or_404(cut_coin, pk=request.POST.get("reward_id"), status=True)
        try:
            redemption = redeem_activity_reward(request.user, reward)
        except InsufficientCoins:
            messages.error(request, "เหรียญยังไม่พอสำหรับแลกรายการนี้")
        except CoinError as error:
            messages.error(request, str(error))
        else:
            messages.success(
                request,
                "แลกสำเร็จ ได้รับ %s ชั่วโมงกิจกรรม เหลือ %s เหรียญ"
                % (redemption.activity_hours, redemption.balance_after),
            )
        return redirect("coins")

    rewards = cut_coin.objects.filter(status=True).order_by("coin", "id")
    transactions = (
        CoinTransaction.objects.filter(user=request.user)
        .select_related("checkin", "redemption", "redemption__cut_coin")
        .order_by("-created_at")[:20]
    )
    redemptions = (
        user_cut_coin.objects.filter(user=request.user)
        .select_related("cut_coin")
        .order_by("-created_at")[:8]
    )
    return render(
        request,
        "checkin/coins.html",
        {
            "wallet": wallet,
            "rewards": rewards,
            "transactions": transactions,
            "redemptions": redemptions,
        },
    )
