import os
import sys
from datetime import datetime
from pprint import pformat

import django


def object_description(object):
    desc = pformat(object, indent=4)
    # print(repr(desc))
    # desc = desc.replace('\n', '<br>')
    return desc


# inspect.object_description = object_description

for p in sys.path:
    x = "/geoluminate/"
    if x in p:
        sys.path.append(p.replace(x, "/"))

sys.path.insert(0, os.path.abspath("../.."))
os.environ["DJANGO_SETTINGS_MODULE"] = "project.settings"
django.setup()

project = "GeoLuminate"
copyright = f"{datetime.now().year}, Sam Jennings"
author = "Sam Jennings"
release = "0.1.0"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.duration",
    # 'sphinx.ext.doctest',
    "sphinx.ext.autodoc",
    "sphinx.ext.todo",
    "sphinx.ext.githubpages",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    # "sphinx_rtd_theme",
]

templates_path = ["_templates"]
exclude_patterns = []
add_module_names = False

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_static_path = ["_static"]
html_favicon = "../../geoluminate/static/geoluminate/icon.svg"
html_logo = "../../geoluminate/static/geoluminate/logo.svg"
html_title = "GeoLuminate"
html_short_title = "GeoLuminate"

html_theme_options = {
    "source_repository": "https://github.com/SSJenny90/geoluminate",
    "source_branch": "development",
    "source_directory": "docs/source/",
}

autodoc_default_options = {
    "exclude-members": "__weakref__",
}
