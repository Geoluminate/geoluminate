#!/usr/bin/env python

import os
import sys
from pathlib import Path

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.settings")
    os.environ.setdefault("DATABASE_URL", "postgresql://username:password@hostname:5555/database_name")

    from django.core.management import execute_from_command_line

    # This allows easy placement of apps within the interior
    # project directory.
    current_path = Path(__file__).parent.resolve()
    sys.path.append(str(current_path / "tests"))

    execute_from_command_line(sys.argv)
