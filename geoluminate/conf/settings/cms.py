from django.utils.translation import gettext_lazy as _

CMS_LANGUAGES = {
    # Customize this
    1: [
        {
            "code": "en",
            "name": _("English"),
            "redirect_on_fallback": True,
            "public": True,
            "hide_untranslated": False,
        },
    ],
    "default": {
        "redirect_on_fallback": True,
        "public": True,
        "hide_untranslated": False,
    },
}
""""""

CMS_TEMPLATES = (
    # Customize this
    ("fullwidth.html", "Fullwidth"),
    ("sidebar_left.html", "Sidebar Left"),
    ("sidebar_right.html", "Sidebar Right"),
)
""""""


# set to true to hide toolbar
# Has unintended side effects when adding plugins.
# Don't use until bug fixed
CMS_TOOLBAR_HIDE = False
""""""

CMS_PERMISSION = False
""""""

CMS_TOOLBAR_ANONYMOUS_ON = False
""""""

CMS_PLACEHOLDER_CONF = {}
""""""

DJANGOCMS_ICON_TEMPLATES = [
    ("svg", "SVG template"),
]
""""""

DJANGOCMS_ICON_SETS = [
    ("fontawesome5regular", "far", "Font Awesome 5 Regular", "lastest"),
    ("fontawesome5solid", "fas", "Font Awesome 5 Solid", "lastest"),
    ("fontawesome5brands", "fab", "Font Awesome 5 Brands", "lastest"),
]
""""""
