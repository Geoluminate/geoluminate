import inspect
import logging
import os
import environ
from pathlib import Path
from split_settings.tools import include

logger = logging.getLogger(__name__)


def setup(apps=[], base_dir=None):
    """Adds all the default variables defined in geoluminate.conf.settings to the global namespace.

    Args:
        development (bool): Whether or not to load development settings. Defaults to False.
    """

    DJANGO_ENV = os.environ.get("DJANGO_ENV")

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
        # read any override config from the .env file
        environ.Env.read_env("stack.development.env")
        logger.info("Loading development settings")
        # env("DJANGO_INSECURE", default=True)
        os.environ.setdefault("DJANGO_INSECURE", "True")
        include(
            "environment.py",
            "settings/general.py",
            "settings/*.py",
            "dev_overrides.py",
            scope=globals,
        )
    else:
        # read any override config from the stack.env file (if it exists)
        environ.Env.read_env("stack.env")
        logger.info("Loading production settings")
        include("settings/general.py", "settings/*.py", scope=globals)
