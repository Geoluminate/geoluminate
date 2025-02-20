from django.db.models.base import Model as Model
from django.utils.translation import gettext as _
from django_filters import FilterSet

from fairdm import plugins
from fairdm.views import FairDMListView

from .forms.organization import RORForm
from .models import Contribution


@plugins.register(to=["project", "dataset", "sample"])
class ContributorsPlugin(FairDMListView):
    template_name = "contributors/contribution_list.html"
    object_template = "contributors/contribution_card.html"
    model = Contribution
    filterset_fields = ["contributor__name"]
    icon = "contributors"
    title = name = _("Contributors")
    ncols = 5
    forms = [RORForm]
    modals = [
        "modals.add_contributor",
        "modals.add_ror",
        "modals.add_orcid",
    ]

    def get_filterset_class(self):
        return FilterSet

    def get_queryset(self, *args, **kwargs):
        return self.base_object.contributors.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["forms"] = {
            "add_contributor_form": RORForm(),
        }
        context["object"] = self.base_object
        context["modals"] = self.modals
        return context
