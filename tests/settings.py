import geoluminate

geoluminate.setup(
    apps=[
        "example",
        # "django_better_admin_arrayfield",
    ]
)

ROOT_URLCONF = "geoluminate.urls"

# DEBUG_TOOLBAR_CONFIG = {
#     # "DISABLE_PANELS": ["debug_toolbar.panels.redirects.RedirectsPanel"],
#     "SHOW_TEMPLATE_CONTEXT": True,
#     "ROOT_TAG_EXTRA_ATTRS": "hx-preserve",
# }

# DEBUG_TOOLBAR_PANELS += [
#     "template_profiler_panel.panels.template.TemplateProfilerPanel",
# ]
