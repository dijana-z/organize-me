import time

from django.db import connection
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to pause execution until the database is available."""

    def handle(self, *args, **options):
        self.stdout.write('Waiting for database...')
        db_connection = None

        while not db_connection:
            try:
                db_connection = connection['default']
            except OperationalError:
                self.stdout.write('Database unavailable, waiting one second.')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!'))
