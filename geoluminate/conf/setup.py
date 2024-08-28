from email.mime import base
import inspect
import logging
import os
import environ
from pathlib import Path
from split_settings.tools import include

logger = logging.getLogger(__name__)

DJANGO_ENV = os.environ.setdefault("DJANGO_ENV", "production")
env = environ.Env.read_env(f"stack.{DJANGO_ENV}.env")


def setup(apps=[], base_dir=None):
    """Adds all the default variables defined in geoluminate.conf.settings to the global namespace.

    Args:
        development (bool): Whether or not to load development settings. Defaults to False.
    """

    globals = inspect.stack()[1][0].f_globals
    if not base_dir:
        base_dir = Path(globals["__file__"]).resolve(strict=True).parent.parent

    globals.update(
        {
            "GEOLUMINATE_APPS": apps,
            "DJANGO_ENV": DJANGO_ENV,
            "BASE_DIR": base_dir,
            "__file__": os.path.realpath(__file__),
        }
    )

    if DJANGO_ENV == "development":
        logger.info("Loading development settings")
        # env("DJANGO_INSECURE", default=True)
        os.environ.setdefault("DJANGO_INSECURE", "True")
        # include("local.py", scope=globals)
        include("settings/general.py", "settings/*.py", "dev_settings.py", scope=globals)

    else:
        logger.info("Loading production settings")
        include("settings/general.py", "settings/*.py", scope=globals)
