from django.utils.translation import gettext_lazy as _

JAZZMIN_SETTINGS = {
    # title of the window
    "site_title": "Geoluminate Admin",
    # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_header": "Geoluminate",
    # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_brand": " ",
    # Logo to use for your site, must be present in static files, used for brand on top left
    "site_logo": "geoluminate/img/brand/logo.svg",
    # Logo to use for your site, must be present in static files, used for login form logo (defaults to site_logo)
    "login_logo": "geoluminate/img/brand/logo.svg",
    # Logo to use for login form in dark themes (defaults to login_logo)
    "login_logo_dark": "geoluminate/img/brand/logo.svg",
    # CSS classes that are applied to the logo above
    # "site_logo_classes": "img-circle",
    "site_logo_classes": "img-thumbnail shadow-none border-0",
    # Relative path to a favicon for your site, will default to site_logo if absent (ideally 32x32 px)
    "site_icon": "geoluminate/img/brand/icon.svg",
    # Welcome text on the login screen
    "welcome_sign": "Welcome to the library",
    # Copyright on the footer
    "copyright": "Geoluminate Ltd",
    # List of model admins to search from the search bar, search bar omitted if excluded
    # If you want to use a single search field you dont need to use a list, you can use a simple string
    # "search_model": ["auth.User", "auth.Group"],
    # Field name on user model that contains avatar ImageField/URLField/Charfield or a callable that receives the user
    "user_avatar": False,
    ############
    # Top Menu #
    ############
    # Links to put along the top menu
    "topmenu_links": [
        # Url that gets reversed (Permissions can be added)
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        {
            "name": "Database",
            "children": [
                {
                    "name": "ERD",
                    "url": "/admin/entity-relationships/",
                },
                {
                    "name": "Metrics",
                    "url": "/admin/postgres-metrics/detailed-index-usage/",
                },
                {"model": "django_celery_beat.PeriodicTask"},
            ],
        },
        # model admin to link to (Permissions checked against model)
        # {"model": "user.User"},
        # App with dropdown menu to all its models pages (Permissions checked against models)
        {
            "name": "CMS",
            "url": "admin:cms_page_changelist",
            "permissions": ["auth.view_user"],
        },
        {
            "name": "Translations",
            "url": "/admin/translate/",
            # "permissions": ["auth.is_super_user"],
        },
    ],
    #############
    # User Menu #
    #############
    # Additional links to include in the user menu on the top right ("app" url type is not allowed)
    "usermenu_links": [
        {
            "name": "Support",
            "url": "https://github.com/GeoLuminate/geoluminate/issues",
            "new_window": True,
        },
        {"model": "user.user"},
    ],
    #############
    # Side Menu #
    #############
    # Whether to display the side menu
    "show_sidebar": True,
    # Whether to aut expand the menu
    "navigation_expanded": True,
    # Hide these apps when generating side menu e.g (auth)
    "hide_apps": [
        "account",
        "socialaccount",
        "taggit",
        "authtoken",
        "cms",
        "invitations",
        "django_celery_beat",
        "filer",
        # "tellme",
        "user",
        "auth",
        "sites",
        # "ror",
        "threadedcomments",
        "licensing",
        "laboratory",
        # "controlled_vocabulary",
        "literature",
        "fluent_comments",
    ],
    "hide_models": [],
    # List of apps (and/or models) to order the side menu
    "order_with_respect_to": ["geoluminate"],
    # Custom links to append to app groups, keyed on app name
    "custom_links": {
        "geoluminate": [
            {
                "name": _("Files"),
                "url": "admin:filer_folder_changelist",
                "icon": "fas fa-folder",
                "permissions": ["user.is_staff"],
            },
            {
                "name": _("Users"),
                "url": "admin:user_user_changelist",
                "icon": "fas fa-user",
                "permissions": ["user.is_staff"],
            },
            {
                "name": _("Groups"),
                "url": "admin:auth_group_changelist",
                "icon": "fas fa-users",
                "permissions": ["user.is_staff"],
            },
            # {
            #     "name": _("Organizations"),
            #     "url": "admin:ror_organization_changelist",
            #     "icon": "fas fa-university",
            #     "permissions": ["user.is_staff"],
            # },
            {
                "name": _("Literature"),
                "url": "admin:literature_literature_changelist",
                "icon": "fas fa-book",
                "permissions": ["user.is_staff"],
            },
            # {
            #     "name": _("Vocabularies"),
            #     "url": "admin:controlled_vocabulary_controlledvocabulary_changelist",
            #     "icon": "fas fa-list",
            #     "permissions": ["user.is_staff"],
            # },
            {
                "name": _("Moderation"),
                "url": "admin:fluent_comments_fluentcomment_changelist",
                "icon": "fas fa-comments",
                "permissions": ["user.is_staff"],
            },
            # {
            #     "name": _("Feedback"),
            #     "url": "admin:tellme_feedback_changelist",
            #     "icon": "fas fa-bullhorn",
            #     "permissions": ["user.is_staff"],
            # },
        ],
        "user": [
            {
                "name": "Invite New",
                "url": "http://127.0.0.1:8000/admin/invitations/invitation/add/",
                "icon": "fas fa-user-plus",
                "permissions": ["user.is_staff"],
            }
        ],
    },
    # Custom icons for side menu apps/models
    # for the full list of 5.13.0 free icon classes
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.User": "fas fa-user",
        "auth.Group": "fas fa-users",
        "literature.Literature": "fas fa-book",
        "literature.Author": "fas fa-users",
        "fluent_comments.fluentcomment": "fas fa-comments",
        "geoluminate.globalconfiguration": "fas fa-cogs",
        "user.User": "fas fa-user",
        # "ror.Organization": "fas fa-university",
        "filer.Folder": "fas fa-file",
        "laboratory.Laboratory": "fas fa-microscope",
        "laboratory.Manufacturer": "fas fa-industry",
    },
    # Icons that are used when one is not manually specified
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    #################
    # Related Modal #
    #################
    # Use modals instead of popups
    "related_modal_active": True,
    #############
    # UI Tweaks #
    #############
    # Relative paths to custom CSS/JS scripts (must be present in static files)
    "custom_css": "geoluminate/css/custom-admin.min.css",
    # "custom_js": "geoluminate/js/custom-admin.js",
    # Whether to link font from fonts.googleapis.com (use custom_css to supply font otherwise)
    "use_google_fonts_cdn": True,
    # Whether to show the UI customizer on the sidebar
    "show_ui_builder": True,
    ###############
    # Change view #
    ###############
    # Render out the change view as a single form, or in tabs, current options are
    # - single
    # - horizontal_tabs (default)
    # - vertical_tabs
    # - collapsible
    # - carousel
    "changeform_format": "vertical_tabs",
    # override change forms on a per modeladmin basis
    "changeform_format_overrides": {
        "auth.user": "collapsible",
        "geoluminate.globalconfiguration": "vertical_tabs",
    },
    # Add a language dropdown into the admin
    # "language_chooser": True,
}

JAZZMIN_UI_TWEAKS = {
    "body_small_text": True,
    "brand_colour": False,
    "accent": "accent-lightblue",
    "navbar": "navbar-dark primary-bg",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "footer_classes": "d-flex justify-content-between align-items-center",
    "sidebar_fixed": True,
    "sidebar": "sidebar-light-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": True,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": True,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": True,
    "theme": "sandstone",
    "dark_mode_theme": "superhero",
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success",
    },
    "actions_sticky_top": True,
}

# Django Admin URL.
ADMIN_URL = "admin/"
