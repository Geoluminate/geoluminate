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
        {
            "code": "en-gb",
            "name": _("English (GB)"),
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


CMS_TOOLBARS = [
    # CMS Toolbars
    "cms.cms_toolbars.PlaceholderToolbar",
    "cms.cms_toolbars.BasicToolbar",
    "cms.cms_toolbars.PageToolbar",
    # third-party Toolbar
    # "geoluminate.cms_toolbars.DjangoCMSToolbarOverride",
]


CMS_ENABLE_HELP = True

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
