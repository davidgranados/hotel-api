"""
Django command to wait for the database to be available.
"""
import time

from django.core.management.base import BaseCommand
from django.db.utils import OperationalError
from psycopg2 import OperationalError as Psycopg2Error


class Command(BaseCommand):
    """Django command to wait for the database."""

    def handle(self, *args, **options):
        """Entrypoint for command."""
        self.stdout.write("Waiting for database...")
        db_up = False
        while db_up is False:
            try:
                self.stdout.write("Checking database...")
                self.check(databases=["default"])
                db_up = True
            except (OperationalError, Psycopg2Error):
                self.stdout.write("Database unavailable, waiting 1 second...")
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS("Database available!"))
