from django.core.management.commands.migrate import Command as MigrationCommand
from django.db import connection


class Command(MigrationCommand):
    def add_arguments(self, parser):
        parser.add_argument("schema", type=str)
        super().add_arguments(parser)

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            schema = options["schema"]
            cursor.execute("CREATE SCHEMA IF NOT EXISTS {}".format(schema))
            cursor.execute("SET search_path to {}".format(schema))
            del options["schema"]
            super(Command, self).handle(*args, **options)
