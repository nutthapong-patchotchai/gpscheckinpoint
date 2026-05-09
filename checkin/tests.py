from datetime import date, datetime, timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from checkin.models.address import Amphur, District, Geography, Province
from checkin.models.checkin import CovidCase, gps, user_cut_coin
from checkin.mock_data import DEMO_PASSWORD, seed_demo_data, seed_timeline_mock_data
from checkin.tracing import RISK_HIGH, RISK_LOW, RISK_MEDIUM, find_contact_summaries
from dormitory.models import Dorm, UserDorm


class CovidTracingTests(TestCase):
    def setUp(self):
        self.geo = Geography.objects.create(name="ภาคเหนือ")
        self.province = Province.objects.create(code="56", name="พะเยา", geo=self.geo)
        self.amphur = Amphur.objects.create(
            code="5601",
            name="เมืองพะเยา",
            geo=self.geo,
            province=self.province,
        )
        self.district = District.objects.create(
            code="560116",
            name="แม่กา",
            geo=self.geo,
            province=self.province,
            amphur=self.amphur,
        )
        self.case_user = User.objects.create_user(username="case-user", password="password")
        self.contact_user = User.objects.create_user(username="contact-user", password="password")
        self.staff_user = User.objects.create_user(
            username="staff-user",
            password="password",
            is_staff=True,
        )

    def make_checkin(self, user, place_name, created_at, latitude="19.030000", longitude="99.900000"):
        item = gps.objects.create(
            user=user,
            place_name=place_name,
            place_address="มหาวิทยาลัยพะเยา",
            latitude=latitude,
            longitude=longitude,
            geo=self.geo,
            province=self.province,
            amphur=self.amphur,
            district=self.district,
            sick7=1,
        )
        gps.objects.filter(pk=item.pk).update(created_at=created_at, updated_at=created_at)
        item.refresh_from_db()
        return item

    def make_case(self):
        return CovidCase.objects.create(
            user=self.case_user,
            status=CovidCase.STATUS_CONFIRMED,
            trace_start_date=date(2026, 5, 1),
            trace_end_date=date(2026, 5, 1),
        )

    def test_same_place_within_four_hours_is_high_risk(self):
        current_timezone = timezone.get_current_timezone()
        case_time = timezone.make_aware(datetime(2026, 5, 1, 9, 0), current_timezone)
        contact_time = case_time + timedelta(hours=2)
        self.make_checkin(self.case_user, "โรงอาหารกลาง", case_time)
        self.make_checkin(self.contact_user, "โรงอาหารกลาง", contact_time)

        summaries = find_contact_summaries(self.make_case())

        self.assertEqual(len(summaries), 1)
        self.assertEqual(summaries[0].risk_level, RISK_HIGH)
        self.assertIn("สถานที่เดียวกัน", summaries[0].primary_reason)

    def test_same_dorm_contact_is_medium_risk_without_contact_checkin(self):
        current_timezone = timezone.get_current_timezone()
        case_time = timezone.make_aware(datetime(2026, 5, 1, 9, 0), current_timezone)
        self.make_checkin(self.case_user, "หอพัก UP", case_time)
        dorm = Dorm.objects.create(
            name="หอพัก UP",
            address="แม่กา",
            geo=self.geo,
            province=self.province,
            amphur=self.amphur,
            district=self.district,
            post="56000",
            tel="0800000000",
            latitude="19.030000",
            longitude="99.900000",
        )
        UserDorm.objects.create(user=self.case_user, dorm=dorm)
        UserDorm.objects.create(user=self.contact_user, dorm=dorm)

        summaries = find_contact_summaries(self.make_case())

        self.assertEqual(len(summaries), 1)
        self.assertEqual(summaries[0].risk_level, RISK_MEDIUM)
        self.assertTrue(summaries[0].same_dorm)
        self.assertEqual(summaries[0].dorm_name, "หอพัก UP")

    def test_staff_can_render_case_detail_and_export_csv(self):
        current_timezone = timezone.get_current_timezone()
        case_time = timezone.make_aware(datetime(2026, 5, 1, 9, 0), current_timezone)
        self.make_checkin(self.case_user, "อาคารเรียนรวม", case_time)
        self.make_checkin(self.contact_user, "อาคารเรียนรวม", case_time + timedelta(hours=1))
        covid_case = self.make_case()
        self.client.force_login(self.staff_user)

        detail_response = self.client.get(reverse("tracing_case_detail", args=[covid_case.pk]))
        self.assertEqual(detail_response.status_code, 200)
        self.assertContains(detail_response, "ผู้เกี่ยวข้องที่ระบบพบ")

        export_response = self.client.get(reverse("tracing_case_export_csv", args=[covid_case.pk]))
        self.assertEqual(export_response.status_code, 200)
        self.assertIn("text/csv", export_response["Content-Type"])
        self.assertIn("อาคารเรียนรวม", export_response.content.decode("utf-8-sig"))


class TimelineMockDataTests(TestCase):
    def test_seed_timeline_mock_data_is_idempotent_and_traceable(self):
        seed_timeline_mock_data()
        result = seed_timeline_mock_data()
        covid_case = result["case"]

        self.assertEqual(
            CovidCase.objects.filter(
                user__username="timeline_case_01",
                notes__contains="[timeline-mock]",
            ).count(),
            1,
        )
        self.assertEqual(gps.objects.filter(user__username__startswith="timeline_").count(), 9)

        summaries = find_contact_summaries(covid_case)
        risk_levels = {summary.risk_level for summary in summaries}
        self.assertIn(RISK_HIGH, risk_levels)
        self.assertIn(RISK_MEDIUM, risk_levels)
        self.assertIn(RISK_LOW, risk_levels)
        self.assertTrue(any(summary.same_dorm for summary in summaries))


class AdminDashboardTests(TestCase):
    def test_admin_index_uses_custom_dashboard(self):
        admin_user = User.objects.create_superuser(
            username="admin-dashboard",
            email="admin-dashboard@example.test",
            password="password12345",
        )
        self.client.force_login(admin_user)

        response = self.client.get(reverse("admin:index"), HTTP_HOST="localhost")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "UP Checkin Control Center")
        self.assertContains(response, "data-dashboard-search")
        self.assertContains(response, "data-dashboard-theme")


class DemoDataTests(TestCase):
    def test_seed_demo_data_builds_full_demo_accounts(self):
        result = seed_demo_data()
        second_result = seed_demo_data()

        demo_user = second_result["user"]
        demo_admin = second_result["admin"]
        wallet = second_result["wallet"]

        self.assertEqual(demo_user.username, "demo_user")
        self.assertTrue(demo_user.check_password(DEMO_PASSWORD))
        self.assertEqual(demo_admin.username, "demo_admin")
        self.assertTrue(demo_admin.is_staff)
        self.assertTrue(demo_admin.is_superuser)
        self.assertTrue(demo_admin.check_password(DEMO_PASSWORD))

        self.assertEqual(gps.objects.filter(user=demo_user).count(), 20)
        self.assertEqual(user_cut_coin.objects.filter(user=demo_user).count(), 1)
        self.assertEqual(wallet.total_earned, 490)
        self.assertEqual(wallet.total_spent, 180)
        self.assertEqual(wallet.balance, 310)
        self.assertEqual(wallet.longest_streak, 20)

        summaries = find_contact_summaries(result["case"])
        risk_levels = {summary.risk_level for summary in summaries}
        self.assertIn(RISK_HIGH, risk_levels)
        self.assertIn(RISK_MEDIUM, risk_levels)
        self.assertIn(RISK_LOW, risk_levels)
        self.assertTrue(any(summary.same_dorm for summary in summaries))
