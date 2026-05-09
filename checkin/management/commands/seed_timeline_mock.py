from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.urls import reverse

from checkin.mock_data import seed_timeline_mock_data


class Command(BaseCommand):
    help = "Seed mock data for the COVID timeline/contact tracing screens."

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Allow seeding when DEBUG is off.",
        )

    def handle(self, *args, **options):
        if not settings.DEBUG and not options["force"]:
            raise CommandError(
                "Refusing to seed timeline mock data while DEBUG is off. "
                "Run with --force only for a controlled non-production database."
            )

        result = seed_timeline_mock_data()
        stats = result["stats"]
        covid_case = result["case"]

        self.stdout.write(
            self.style.SUCCESS(
                "Seeded timeline mock data: case #%s, %s check-ins, %s users created."
                % (
                    covid_case.pk,
                    len(result["checkins"]),
                    stats["users_created"],
                )
            )
        )
        self.stdout.write("Case detail: %s" % reverse("tracing_case_detail", args=[covid_case.pk]))
        self.stdout.write(
            "Timeline user: timeline_case_01; staff marker user: timeline_staff"
        )
        self.stdout.write(
            "Mock users are created without usable passwords; use an existing staff/admin account."
        )
