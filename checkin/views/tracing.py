import csv

from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from checkin.forms import CovidCaseForm
from checkin.models.checkin import CovidCase
from checkin.tracing import (
    find_contact_summaries,
    get_case_checkins,
    get_case_window,
    get_current_dorm,
    get_tracing_overview,
)


def staff_required(view_func):
    return user_passes_test(lambda user: user.is_staff, login_url="login")(view_func)


@staff_required
def dashboard(request):
    cases = (
        CovidCase.objects.select_related("user", "created_by")
        .all()
        .order_by("-updated_at", "-created_at")[:60]
    )
    return render(
        request,
        "checkin/tracing/dashboard.html",
        {
            "cases": cases,
            "overview": get_tracing_overview(),
        },
    )


@staff_required
def case_create(request):
    form = CovidCaseForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        covid_case = form.save(commit=False)
        covid_case.created_by = request.user
        covid_case.save()
        messages.success(request, "บันทึกเคสเรียบร้อยแล้ว ระบบสร้าง timeline ให้ทันที")
        return redirect("tracing_case_detail", pk=covid_case.pk)

    return render(
        request,
        "checkin/tracing/case_form.html",
        {
            "form": form,
            "mode": "create",
        },
    )


@staff_required
def case_update(request, pk):
    covid_case = get_object_or_404(CovidCase.objects.select_related("user"), pk=pk)
    form = CovidCaseForm(request.POST or None, instance=covid_case)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "อัปเดตเคสเรียบร้อยแล้ว")
        return redirect("tracing_case_detail", pk=covid_case.pk)

    return render(
        request,
        "checkin/tracing/case_form.html",
        {
            "form": form,
            "case": covid_case,
            "mode": "edit",
        },
    )


@staff_required
def case_detail(request, pk):
    covid_case = get_object_or_404(CovidCase.objects.select_related("user", "created_by"), pk=pk)
    timeline = list(get_case_checkins(covid_case))
    contact_summaries = find_contact_summaries(covid_case)
    start_date, end_date = get_case_window(covid_case)
    return render(
        request,
        "checkin/tracing/case_detail.html",
        {
            "case": covid_case,
            "timeline": timeline,
            "contact_summaries": contact_summaries,
            "trace_start_date": start_date,
            "trace_end_date": end_date,
            "current_dorm": get_current_dorm(covid_case.user),
        },
    )


def format_datetime(value):
    if not value:
        return ""
    return timezone.localtime(value).strftime("%d/%m/%Y %H:%M")


def checkin_fields(item):
    if item is None:
        return {
            "date_time": "",
            "place": "",
            "address": "",
            "district": "",
            "amphur": "",
            "province": "",
            "latitude": "",
            "longitude": "",
            "checkin_id": "",
        }

    return {
        "date_time": format_datetime(item.created_at),
        "place": item.location_label,
        "address": item.place_address,
        "district": item.district.name if item.district else "",
        "amphur": item.amphur.name if item.amphur else "",
        "province": item.province.name if item.province else "",
        "latitude": item.latitude,
        "longitude": item.longitude,
        "checkin_id": item.id,
    }


@staff_required
def case_export_csv(request, pk):
    covid_case = get_object_or_404(CovidCase.objects.select_related("user"), pk=pk)
    timeline = list(get_case_checkins(covid_case))
    contact_summaries = find_contact_summaries(covid_case)

    response = HttpResponse(content_type="text/csv")
    filename = "covid-case-%s-timeline.csv" % covid_case.pk
    response["Content-Disposition"] = 'attachment; filename="%s"; encoding="utf-8-sig"' % filename
    response.write("\ufeff")

    writer = csv.writer(response)
    writer.writerow(
        [
            "ประเภท",
            "ผู้ใช้",
            "สถานะ/ความเสี่ยง",
            "วันเวลา",
            "สถานที่",
            "ที่อยู่",
            "ตำบล",
            "อำเภอ",
            "จังหวัด",
            "latitude",
            "longitude",
            "เหตุผล",
            "ระยะห่างกม.",
            "เวลาห่างนาที",
            "case_checkin_id",
            "contact_checkin_id",
        ]
    )

    for item in timeline:
        fields = checkin_fields(item)
        writer.writerow(
            [
                "timeline",
                covid_case.owner_name,
                covid_case.get_status_display(),
                fields["date_time"],
                fields["place"],
                fields["address"],
                fields["district"],
                fields["amphur"],
                fields["province"],
                fields["latitude"],
                fields["longitude"],
                "timeline ของเคส",
                "",
                "",
                fields["checkin_id"],
                "",
            ]
        )

    for summary in contact_summaries:
        for match in summary.matches:
            contact_fields = checkin_fields(match.contact_checkin)
            case_fields = checkin_fields(match.case_checkin)
            writer.writerow(
                [
                    "contact",
                    summary.user.get_full_name() or summary.user.username,
                    match.risk_label,
                    contact_fields["date_time"],
                    contact_fields["place"],
                    contact_fields["address"],
                    contact_fields["district"],
                    contact_fields["amphur"],
                    contact_fields["province"],
                    contact_fields["latitude"],
                    contact_fields["longitude"],
                    match.reason,
                    "%.2f" % match.distance_km if match.distance_km is not None else "",
                    match.time_gap_minutes if match.time_gap_minutes is not None else "",
                    case_fields["checkin_id"],
                    contact_fields["checkin_id"],
                ]
            )

    return response
