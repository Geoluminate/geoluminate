import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.resolve()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.settings")

os.environ["GEOLUMINATE_CONFIG_PATH"] = str(BASE_DIR / "geoluminate.yml")
sys.path.append(str(BASE_DIR / "tests"))


from docs.conf import *

# https://sphinx-book-theme.readthedocs.io/en/stable/reference.html
# https://pydata-sphinx-theme.readthedocs.io/en/latest/user_guide/index.html
html_theme_options.update(
    {
        "announcement": (
            "⚠️Geoluminate is currently undergoing rapid development and the API may change without notice! ⚠️"
        ),
    }
)

# exclude_patterns = ["apidocs/index.rst"]

# # despite the fact that extensions is declared in docs/conf.py, and is definitely available here (see print(extensions)),
# # the build will not work without declaring the extensions variable here as well.
extensions = [
    "sphinx.ext.viewcode",
    "sphinx.ext.duration",
    # 'sphinx.ext.doctest',
    "sphinx.ext.todo",
    "sphinx.ext.githubpages",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx.ext.autosectionlabel",
    "sphinx_copybutton",
    "sphinxext.opengraph",
    # "autodoc2",
    # "sphinx_comments",
    "myst_parser",
    # "sphinx_tippy",
]
