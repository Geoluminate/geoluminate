#!/usr/bin/env python

import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_ENV", "development")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.settings")
    # os.environ.setdefault("DATABASE_URL", "postgresql://username:password@hostname:5555/database_name")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
