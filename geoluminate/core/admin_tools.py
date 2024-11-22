import os

from admin_tools.dashboard import AppIndexDashboard, Dashboard, modules
from admin_tools.menu import Menu, items
from django.conf import settings
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from easy_icons.templatetags.easy_icons import icon

GEOLUMINATE_APPS = {f.split(".")[0] for f in settings.GEOLUMINATE_APPS}


class CustomIndexDashboard(Dashboard):
    def init_with_context(self, context):
        # site_name = get_admin_site_name(context)
        # append a link list module for "quick links"
        # self.children.append(
        #     modules.LinkList(
        #         _("Quick links"),
        #         layout="inline",
        #         # draggable=False,
        #         # deletable=False,
        #         collapsible=False,
        #         children=[
        #             [_("Return to site"), "/"],
        #             [_("Change password"), reverse("%s:password_change" % site_name)],
        #             [_("Log out"), reverse("%s:logout" % site_name)],
        #         ],
        #     )
        # )

        self.children.append(
            modules.ModelList(
                title=_("Geoluminate"),
                models=[
                    "geoluminate.contrib.core.models.Project",
                    "geoluminate.contrib.core.models.Dataset",
                    "geoluminate.contrib.core.models.Sample",
                    "geoluminate.contrib.core.models.Measurement",
                    "geoluminate.contrib.gis.models.Location",
                ],
            )
        )

        self.children.append(
            modules.ModelList(
                title=_("Reference management"),
                models=["literature.models.*"],
            )
        )

        self.children.append(
            modules.ModelList(
                title=_("Laboratories"),
                models=[
                    "laboratory.models.Laboratory",
                    "laboratory.models.Instrument",
                ],
            )
        )

        # self.children.append(
        #     modules.ModelList(
        #         title=_("Community"),
        #         models=[
        #             # "invitations.models.*",
        #             "geoluminate.contrib.users.models.User",
        #             "geoluminate.contrib.organizations.models.Organization",
        #         ],
        #     )
        # )

        self.children.append(
            modules.ModelList(
                title=_("Accounts"),
                models=[
                    "django.contrib.auth.*",
                    "allauth.account.*",
                    "allauth.socialaccount.models.SocialAccount",
                    "rest_framework.authtoken.*",
                ],
            )
        )

        # self.children.append(
        #     modules.ModelList(
        #         title=_("Configuration"),
        #         models=[
        #             "configuration.models.*",
        #             "django_celery_beat.models.PeriodicTask",
        #             "django.contrib.sites.*",
        #             "allauth.socialaccount.models.SocialApp",
        #             "allauth.socialaccount.models.SocialToken",
        #         ],
        #     )
        # )

        # append a recent actions module
        self.children.append(modules.RecentActions(_("Recent Actions"), 5))

        # # append a feed module
        # self.children.append(
        #     modules.Feed(_("Latest Django News"), feed_url="http://www.djangoproject.com/rss/weblog/", limit=5)
        # )

        # append another link list module for "support".
        self.children.append(
            modules.LinkList(
                _("Support"),
                children=[
                    {
                        "title": _("Geoluminate documentation"),
                        "url": "http://docs.geoluminate.net/",
                        "external": True,
                    },
                    {
                        "title": _("Media Files"),
                        "url": os.environ.get("S3_CUSTOM_DOMAIN", ""),
                        "external": True,
                    },
                    # {
                    #     "title": _('Django "django-users" mailing list'),
                    #     "url": "http://groups.google.com/group/django-users",
                    #     "external": True,
                    # },
                    # {
                    #     "title": _("Django irc channel"),
                    #     "url": "irc://irc.freenode.net/django",
                    #     "external": True,
                    # },
                ],
            )
        )


class CustomAppIndexDashboard(AppIndexDashboard):
    title = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.children += [
            modules.ModelList(self.app_title, self.models),
            modules.RecentActions(_("Recent Actions"), include_list=self.get_app_content_types(), limit=5),
        ]

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        return super().init_with_context(context)


class CustomMenu(Menu):
    """
    Custom Menu for geoluminate admin site.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.children += [
            items.MenuItem(_("Dashboard"), reverse("admin:index")),
            items.Bookmarks(),
            items.AppList(
                _("Apps"),
                models=[f"{f}.*" for f in GEOLUMINATE_APPS],
            ),
            items.ModelList(
                _("Configuration"),
                models=[
                    "geoluminate.contrib.identity.models.*",
                    "django_celery_beat.models.PeriodicTask",
                    "django.contrib.sites.*",
                    "allauth.socialaccount.models.SocialApp",
                    "allauth.socialaccount.models.SocialToken",
                ],
            ),
            items.ModelList(
                icon("community"),
                models=(
                    "geoluminate.contrib.contributors.models.Person",
                    "geoluminate.contrib.contributors.models.Organization",
                ),
            ),
            items.ModelList(
                icon("comments"),
                models=("django_comments_xtd.models.*",),
            ),
            # items.AppList(_("Administration"), models=("django.contrib.*",)),
            # items.MenuItem(icon("invite"), reverse("admin:invitations_invitation_add")),
            # items.MenuItem(
            #     _("Invite"),
            #     children=[
            #         items.MenuItem(_("Organization manager"), reverse("admin:datasets_dataset_changelist")),
            #     ],
            # ),
        ]

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        return super().init_with_context(context)
