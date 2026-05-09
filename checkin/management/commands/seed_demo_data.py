from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.urls import reverse

from checkin.mock_data import DEMO_PASSWORD, seed_demo_data


class Command(BaseCommand):
    help = "Seed full demo data for demo_user and demo_admin."

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Allow seeding when DEBUG is off.",
        )

    def handle(self, *args, **options):
        if not settings.DEBUG and not options["force"]:
            raise CommandError(
                "Refusing to seed demo data while DEBUG is off. "
                "Run with --force only for a controlled non-production database."
            )

        result = seed_demo_data()
        stats = result["stats"]
        covid_case = result["case"]
        wallet = result["wallet"]

        self.stdout.write(self.style.SUCCESS("Seeded full demo data."))
        self.stdout.write("demo_admin / %s" % DEMO_PASSWORD)
        self.stdout.write("demo_user / %s" % DEMO_PASSWORD)
        self.stdout.write(
            "Check-ins: %s, contact check-ins: %s, wallet balance: %s"
            % (stats["checkins"], stats["contact_checkins"], wallet.balance)
        )
        self.stdout.write("Tracing dashboard: %s" % reverse("tracing_dashboard"))
        self.stdout.write("Demo case detail: %s" % reverse("tracing_case_detail", args=[covid_case.pk]))
