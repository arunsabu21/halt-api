from django.core.management.base import BaseCommand
from authentication.models import User


class Command(BaseCommand):
    help = "Creates a superuser from env vars, safe to run multiple times."

    def handle(self, *args, **options):
        import os

        email = os.environ.get("ADMIN_EMAIL")
        password = os.environ.get("ADMIN_PASSWORD")

        if not email and password:
            self.stdout.write(
                self.style.ERROR("Set ADMIN_EMAIL and ADMIN_PASSWORD env vars first.")
            )
            return

        if User.objects.filter(email=email).exists():
            self.stdout.write("Admin already exists.")
            return

        User.objects.create_superuser(email=email, password=password)
        self.stdout.write(self.style.SUCCESS(f"Superuser {email} created successfully."))