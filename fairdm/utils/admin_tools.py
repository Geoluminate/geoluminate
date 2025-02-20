import os

from admin_tools.dashboard import AppIndexDashboard, Dashboard, modules
from admin_tools.menu import Menu, items
from django.conf import settings
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from fairdm.registry import registry

FAIRDM_APPS = {f.split(".")[0] for f in settings.FAIRDM_APPS}


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
                title="FairDM",
                models=[
                    "fairdm.core.models.project.Project",
                    "fairdm.core.models.dataset.Dataset",
                ],
            )
        )

        self.children.append(
            modules.AppList(
                title="FairDM" + " " + _("Samples"),
                models=[m["path"] for m in registry.samples],
            )
        )

        self.children.append(
            modules.AppList(
                title="FairDM" + " " + _("Measurements"),
                models=[m["path"] for m in registry.measurements],
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
        #             "fairdm.contrib.users.models.User",
        #             "fairdm.contrib.organizations.models.Organization",
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
                        "title": _("FairDM documentation"),
                        "url": "http://docs.fairdm.net/",
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
    Custom Menu for fairdm admin site.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.children += [
            items.MenuItem(_("Dashboard"), reverse("admin:index")),
            # items.Bookmarks(),
            items.AppList(
                _("Add-ons"),
                models=[f"{f}.*" for f in FAIRDM_APPS],
            ),
            items.ModelList(
                _("Configuration"),
                models=[
                    "fairdm.contrib.identity.models.*",
                    "django_celery_beat.models.PeriodicTask",
                    "django.contrib.sites.*",
                    "allauth.socialaccount.models.SocialApp",
                    "allauth.socialaccount.models.SocialToken",
                ],
            ),
            items.ModelList(
                _("Community"),
                models=(
                    "fairdm.contrib.contributors.models.Person",
                    "fairdm.contrib.contributors.models.Organization",
                ),
            ),
            items.ModelList(
                _("Comments"),
                models=("django_comments_xtd.models.*",),
            ),
            items.MenuItem(_("Reference Manager"), reverse("literature-list")),
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
