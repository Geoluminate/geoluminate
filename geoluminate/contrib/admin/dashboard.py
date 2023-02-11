# """Contains a single class derived from `Django Grappelli`_'s
# ``dashboard.Dashboard`` class which is used to configure the
# dashboard of the admin site. For configuration options, visit
# the Django Grappelli `dasboard API`_.

# Sometimes it can be useful to disable the dashboard and revert back to
# Django Grappelli's standard view (e.g. for debugging if new applications
# are not showing in the admin view). To do so, set::

#     # in your settings.py file
#     GRAPPELLI_INDEX_DASHBOARD = None

# .. _Django Grappelli: link: https://domain.invalid/
# .. _dasboard API: link: https://django-grappelli.readthedocs.io/en/latest/dashboard_api.html
# """
# from django.utils.translation import gettext_lazy as _
# from grappelli.dashboard import Dashboard, modules
# from grappelli.dashboard.modules import AppList, Group, ModelList

# from geoluminate.conf import settings

# from ...utils import get_db_name


# class AdminDashboard(Dashboard):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)

#         self.children.append(
#             ModelList(
#                 get_db_name(),
#                 column=1,
#                 collapsible=True,
#                 models=("database*",),
#             )
#         )

#         self.children.append(
#             ModelList(
#                 _("Literature Management"),
#                 column=1,
#                 collapsible=True,
#                 models=(
#                     "literature*",
#                     "crossref*",
#                 ),
#             )
#         )

#         self.children.append(
#             ModelList(
#                 _("Random"),
#                 column=2,
#                 collapsible=True,
#                 models=("*",),
#             )
#         )
#         self.children.append(
#             ModelList(
#                 _("Instruments"),
#                 column=2,
#                 collapsible=True,
#                 models=(
#                     "django_laboratory.*",
#                     "*nstrument*",
#                 ),
#             ),
#         )

#         self.children.append(
#             ModelList(
#                 _("Licenses"), column=2, collapsible=True, models=("licensing.*",)
#             ),
#         )

#         self.children.append(
#             Group(
#                 _("Django Earth Science"),
#                 column=1,
#                 collapsible=True,
#                 children=[
#                     ModelList(
#                         _("GIS Plugins"),
#                         column=1,
#                         collapsible=True,
#                         models=("geoscience.gis*",),
#                     ),
#                     ModelList(_("Vocabularies"), models=("geoscience.vocab*",)),
#                 ],
#             )
#         )

#         self.children.append(
#             Group(
#                 _("Configuration"),
#                 column=2,
#                 collapsible=False,
#                 children=[
#                     ModelList(
#                         _("Global"),
#                         column=1,
#                         collapsible=False,
#                         models=("geoluminate*",),
#                     ),
#                 ],
#             )
#         )

#         self.children.append(
#             ModelList(
#                 _("GFZ Dataservices"),
#                 column=1,
#                 collapsible=True,
#                 models=("datacite*",),
#             )
#         )

#         self.children.append(
#             ModelList(
#                 _("Controlled Vocabulary"),
#                 column=2,
#                 collapsible=True,
#                 models=("controlled*",),
#             )
#         )

#         self.children.append(
#             ModelList(
#                 _("Discussions"),
#                 column=2,
#                 collapsible=True,
#                 models=(
#                     "fluent*",
#                     "tellme*"
#                     #   'threaded*'
#                 ),
#             )
#         )

#         self.children.append(
#             Group(
#                 _("Users and Authentication"),
#                 column=3,
#                 collapsible=True,
#                 children=[
#                     ModelList(
#                         _("Authentication"),
#                         column=3,
#                         collapsible=True,
#                         models=(
#                             "user*",
#                             "django.contrib.*",
#                             "invitations.*",
#                             "allauth.*",
#                         ),
#                     ),
#                     ModelList(
#                         _("Research Organizations"),
#                         column=2,
#                         collapsible=True,
#                         models=("ror.*",),
#                     ),
#                 ],
#             )
#         )

#         self.children.append(
#             ModelList(
#                 _("CMS"),
#                 column=3,
#                 collapsible=True,
#                 models=("cms*",),
#             )
#         )

#         self.children.append(
#             ModelList(
#                 _("Files"),
#                 column=3,
#                 collapsible=True,
#                 models=(
#                     "filer*",
#                     "easy_thumbnails*",
#                 ),
#             )
#         )
