from django.db.models.base import Model as Model
from django.utils.translation import gettext as _

from geoluminate import plugins
from geoluminate.core.view_mixins import ListPluginMixin

from .forms.organization import RORForm


@plugins.register(to=["project", "dataset", "sample"])
class ContributorsPlugin(ListPluginMixin):
    template_name = "contributors/contribution_list.html"
    object_template = "contributors/contribution_card.html"
    icon = "contributors"
    title = name = _("Contributors")
    ncols = 5
    forms = [RORForm]

    def get_queryset(self, *args, **kwargs):
        return self.base_object.contributors.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["forms"] = {
            # "contributor": ContributorForm(),
            # "orcid": ORCIDForm(),
            "ror": RORForm(),
            # "manual_add": ManualAddForm(),
        }
        context["object"] = self.base_object
        return context
