from django.core.management.base import BaseCommand
from authentication.models import User
import os


class Command(BaseCommand):
    help = "Creates a superuser from env vars, safe to run multiple times."

    def handle(self, *args, **options):

        email = os.environ.get("ADMIN_EMAIL")
        password = os.environ.get("ADMIN_PASSWORD")

        if not email and password:
            self.stdout.write(
                self.style.ERROR("Set ADMIN_EMAIL and ADMIN_PASSWORD env vars first.")
            )
            return

        user = User.objects.filter(email=email).first()

        if user:
            if user.is_superuser:
                self.stdout.write("Superuser already exists.")
                return
            user.is_superuser = True
            user.is_staff = True
            user.set_password(password)
            user.save()
            self.stdout.write(
                self.style.SUCCESS(f"Existing user {email} promoted to superuser.")
            )
            return

        User.objects.create_superuser(email=email, password=password)
        self.stdout.write(
            self.style.SUCCESS(f"Superuser {email} created successfully.")
        )
