from django.utils.translation import gettext_lazy as _

# CMS_LANGUAGES = {
#     # Customize this
#     1: [
#         {
#             "code": "en",
#             "name": _("English"),
#             "redirect_on_fallback": True,
#             "public": True,
#             "hide_untranslated": False,
#         },
#         {
#             "code": "en-gb",
#             "name": _("English (GB)"),
#             "redirect_on_fallback": True,
#             "public": True,
#             "hide_untranslated": False,
#         },
#     ],
#     "default": {
#         "redirect_on_fallback": True,
#         "public": True,
#         "hide_untranslated": False,
#     },
# }
""""""

CMS_TEMPLATES = (
    # Customize this
    ("cms/layouts/basic.html", "Basic"),
)
""""""


# CMS_TOOLBARS = [
#     # CMS Toolbars
#     # "cms.cms_toolbars.PlaceholderToolbar",
#     "cms.cms_toolbars.BasicToolbar",
#     "cms.cms_toolbars.PageToolbar",
# ]


CMS_ENABLE_HELP = True

CMS_PERMISSION = False
""""""

CMS_TOOLBAR_ANONYMOUS_ON = False
""""""

CMS_PLACEHOLDER_CONF = {}
""""""

CMS_CONFIRM_VERSION4 = True
""""""
