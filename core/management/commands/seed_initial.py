from django.core.management.base import BaseCommand

from content.seed import seed_all


class Command(BaseCommand):
    help = "Seed Rajbari district/upazilas, staff groups, site content and sample campaigns (idempotent)."

    def handle(self, *args, **options):
        seed_all()
        self.stdout.write(self.style.SUCCESS("Seed complete."))
