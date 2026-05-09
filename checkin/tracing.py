from dataclasses import dataclass, field
from math import asin, cos, radians, sin, sqrt

from django.utils import timezone

from checkin.models.checkin import CovidCase, gps
from checkin.services import get_day_bounds
from dormitory.models import UserDorm


RISK_HIGH = "high"
RISK_MEDIUM = "medium"
RISK_LOW = "low"

RISK_LABELS = {
    RISK_HIGH: "เสี่ยงสูง",
    RISK_MEDIUM: "เสี่ยงกลาง",
    RISK_LOW: "เสี่ยงต่ำ",
}
RISK_ORDER = {
    RISK_HIGH: 3,
    RISK_MEDIUM: 2,
    RISK_LOW: 1,
}


@dataclass
class ContactMatch:
    risk_level: str
    risk_score: int
    reason: str
    case_checkin: gps | None = None
    contact_checkin: gps | None = None
    distance_km: float | None = None
    time_gap_minutes: int | None = None

    @property
    def risk_label(self):
        return RISK_LABELS.get(self.risk_level, self.risk_level)

    @property
    def risk_class(self):
        return self.risk_level


@dataclass
class ContactSummary:
    user: object
    risk_level: str = RISK_LOW
    risk_score: int = 0
    matches: list[ContactMatch] = field(default_factory=list)
    same_dorm: bool = False
    dorm_name: str = ""

    @property
    def risk_label(self):
        return RISK_LABELS.get(self.risk_level, self.risk_level)

    @property
    def risk_class(self):
        return self.risk_level

    @property
    def match_count(self):
        return len(self.matches)

    @property
    def latest_match_at(self):
        dates = [
            match.contact_checkin.created_at
            for match in self.matches
            if match.contact_checkin is not None
        ]
        return max(dates) if dates else None

    @property
    def primary_reason(self):
        if not self.matches:
            return "-"
        return self.matches[0].reason

    def add_match(self, match):
        self.matches.append(match)
        if (
            RISK_ORDER.get(match.risk_level, 0) > RISK_ORDER.get(self.risk_level, 0)
            or match.risk_score > self.risk_score
        ):
            self.risk_level = match.risk_level
            self.risk_score = match.risk_score


def get_case_window(case):
    start_date = case.effective_trace_start_date
    end_date = case.effective_trace_end_date
    if end_date < start_date:
        start_date, end_date = end_date, start_date
    return start_date, end_date


def get_case_day_bounds(case):
    start_date, end_date = get_case_window(case)
    start_at, _ = get_day_bounds(start_date)
    _, end_next = get_day_bounds(end_date)
    return start_at, end_next


def get_case_checkins(case):
    start_at, end_at = get_case_day_bounds(case)
    return (
        gps.objects.filter(
            user=case.user,
            created_at__gte=start_at,
            created_at__lt=end_at,
        )
        .select_related("user", "geo", "province", "amphur", "district")
        .order_by("created_at", "id")
    )


def get_current_dorm(user):
    return (
        UserDorm.objects.filter(user=user)
        .select_related("dorm", "dorm__province", "dorm__amphur", "dorm__district")
        .order_by("-created_at")
        .first()
    )


def normalize_text(value):
    return " ".join((value or "").strip().lower().split())


def parse_coordinate(value):
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number


def has_usable_coordinates(item):
    latitude = parse_coordinate(item.latitude)
    longitude = parse_coordinate(item.longitude)
    if latitude is None or longitude is None:
        return False
    return not (abs(latitude) < 0.0001 and abs(longitude) < 0.0001)


def distance_km(first, second):
    if not has_usable_coordinates(first) or not has_usable_coordinates(second):
        return None

    lat1 = parse_coordinate(first.latitude)
    lng1 = parse_coordinate(first.longitude)
    lat2 = parse_coordinate(second.latitude)
    lng2 = parse_coordinate(second.longitude)
    radius = 6371
    dlat = radians(lat2 - lat1)
    dlng = radians(lng2 - lng1)
    a = (
        sin(dlat / 2) ** 2
        + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlng / 2) ** 2
    )
    return 2 * radius * asin(sqrt(a))


def local_date(item):
    return timezone.localtime(item.created_at).date()


def time_gap_minutes(first, second):
    return int(abs((first.created_at - second.created_at).total_seconds()) // 60)


def same_place(first, second):
    first_label = normalize_text(first.place_name)
    second_label = normalize_text(second.place_name)
    return bool(first_label and second_label and first_label == second_label)


def evaluate_contact_match(case_checkin, contact_checkin):
    same_day = local_date(case_checkin) == local_date(contact_checkin)
    if not same_day:
        return None

    gap = time_gap_minutes(case_checkin, contact_checkin)
    distance = distance_km(case_checkin, contact_checkin)

    if same_place(case_checkin, contact_checkin):
        if gap <= 240:
            return ContactMatch(
                risk_level=RISK_HIGH,
                risk_score=95,
                reason="เช็คอินสถานที่เดียวกันภายใน 4 ชั่วโมง",
                case_checkin=case_checkin,
                contact_checkin=contact_checkin,
                distance_km=distance,
                time_gap_minutes=gap,
            )
        return ContactMatch(
            risk_level=RISK_MEDIUM,
            risk_score=75,
            reason="เช็คอินสถานที่เดียวกันในวันเดียวกัน",
            case_checkin=case_checkin,
            contact_checkin=contact_checkin,
            distance_km=distance,
            time_gap_minutes=gap,
        )

    if distance is not None:
        if distance <= 0.10 and gap <= 240:
            return ContactMatch(
                risk_level=RISK_HIGH,
                risk_score=90,
                reason="พิกัดใกล้กันไม่เกิน 100 เมตรภายใน 4 ชั่วโมง",
                case_checkin=case_checkin,
                contact_checkin=contact_checkin,
                distance_km=distance,
                time_gap_minutes=gap,
            )
        if distance <= 0.25:
            return ContactMatch(
                risk_level=RISK_MEDIUM,
                risk_score=65,
                reason="พิกัดใกล้กันไม่เกิน 250 เมตรในวันเดียวกัน",
                case_checkin=case_checkin,
                contact_checkin=contact_checkin,
                distance_km=distance,
                time_gap_minutes=gap,
            )
        if distance <= 0.50:
            return ContactMatch(
                risk_level=RISK_LOW,
                risk_score=35,
                reason="พิกัดอยู่ในพื้นที่ใกล้เคียงไม่เกิน 500 เมตร",
                case_checkin=case_checkin,
                contact_checkin=contact_checkin,
                distance_km=distance,
                time_gap_minutes=gap,
            )

    if case_checkin.district_id and case_checkin.district_id == contact_checkin.district_id:
        return ContactMatch(
            risk_level=RISK_LOW,
            risk_score=30,
            reason="เช็คอินในตำบลเดียวกันในวันเดียวกัน",
            case_checkin=case_checkin,
            contact_checkin=contact_checkin,
            time_gap_minutes=gap,
        )

    return None


def sort_matches(matches):
    return sorted(
        matches,
        key=lambda item: (
            RISK_ORDER.get(item.risk_level, 0),
            item.risk_score,
            item.contact_checkin.created_at if item.contact_checkin else timezone.now(),
        ),
        reverse=True,
    )


def find_contact_summaries(case):
    case_checkins = list(get_case_checkins(case))
    if not case_checkins:
        return []

    start_at, end_at = get_case_day_bounds(case)
    contact_checkins = (
        gps.objects.filter(created_at__gte=start_at, created_at__lt=end_at)
        .exclude(user=case.user)
        .select_related("user", "geo", "province", "amphur", "district")
        .order_by("created_at", "id")
    )

    summaries = {}
    for contact_checkin in contact_checkins:
        best_match = None
        for case_checkin in case_checkins:
            match = evaluate_contact_match(case_checkin, contact_checkin)
            if match is None:
                continue
            if best_match is None or match.risk_score > best_match.risk_score:
                best_match = match

        if best_match is None:
            continue

        summary = summaries.setdefault(
            contact_checkin.user_id,
            ContactSummary(user=contact_checkin.user),
        )
        summary.add_match(best_match)

    add_same_dorm_contacts(case, summaries)
    for summary in summaries.values():
        summary.matches = sort_matches(summary.matches)

    return sorted(
        summaries.values(),
        key=lambda item: (
            RISK_ORDER.get(item.risk_level, 0),
            item.risk_score,
            item.latest_match_at or timezone.now(),
            item.user.username,
        ),
        reverse=True,
    )


def add_same_dorm_contacts(case, summaries):
    case_dorm = get_current_dorm(case.user)
    if case_dorm is None:
        return

    dorm_users = (
        UserDorm.objects.filter(dorm=case_dorm.dorm)
        .exclude(user=case.user)
        .select_related("user", "dorm")
        .order_by("user__username")
    )
    for user_dorm in dorm_users:
        summary = summaries.setdefault(
            user_dorm.user_id,
            ContactSummary(user=user_dorm.user),
        )
        summary.same_dorm = True
        summary.dorm_name = user_dorm.dorm.name
        if RISK_ORDER.get(summary.risk_level, 0) < RISK_ORDER[RISK_MEDIUM]:
            summary.add_match(
                ContactMatch(
                    risk_level=RISK_MEDIUM,
                    risk_score=60,
                    reason="อยู่หอพักเดียวกันกับเคส",
                )
            )


def get_tracing_overview():
    return {
        "total_cases": CovidCase.objects.count(),
        "confirmed_cases": CovidCase.objects.filter(status=CovidCase.STATUS_CONFIRMED).count(),
        "suspected_cases": CovidCase.objects.filter(status=CovidCase.STATUS_SUSPECTED).count(),
    }
