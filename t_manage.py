#!/usr/bin/env python
import os
import sys
import dotenv

"""
The command will look like:
    python t_manage.py migrate_one schema:aSchemaName
"""
if __name__ == "__main__":
    dotenv.read_dotenv()
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE", "practice_platform_backend.settings.dev"
    )
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    from django.db import connection

    args = sys.argv
    schema = None
    for i, each in enumerate(args):
        if each.find("schema:") != -1:
            schema = each.split(":")[1]
            args.pop(i)
            break
    with connection.cursor() as cursor:
        if schema:
            cursor.execute("SET search_path to {}".format(schema))
            print("Current Schema: {}".format(schema))
        execute_from_command_line(args)
