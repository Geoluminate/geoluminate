from django.utils.translation import gettext_lazy as _

import fairdm

fairdm.setup(apps=["example"])

LANGUAGES = [
    ("en", _("English")),
    ("de", _("German")),
]
