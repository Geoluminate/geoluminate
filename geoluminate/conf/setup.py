import inspect
import logging
import os
from pathlib import Path

from split_settings.tools import include

logger = logging.getLogger(__name__)


def setup(development=False):
    """Adds all the default variables defined in geoluminate.conf.settings to the global namespace.

    Args:
        development (bool): Whether or not to load development settings. Defaults to False.
    """

    # get global variables from the calling module
    globs = inspect.stack()[1][0].f_globals

    # add a BASE_DIR variable to the global namespace
    if not globs.get("BASE_DIR"):
        globs["BASE_DIR"] = (
            Path(globs["__file__"]).resolve(strict=True).parent.parent.parent
        )

    # django-split-settings requires that the __file__ global variable is set relative to the current file
    globs["__file__"] = os.path.realpath(__file__)

    if development:
        logger.info("Loading development settings")
        include("local.py", scope=globs)
    else:
        logger.info("Loading production settings")
        include("production.py", scope=globs)
