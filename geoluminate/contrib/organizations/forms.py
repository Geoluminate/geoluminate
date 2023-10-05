from django import forms
from django.utils.translation import gettext as _
from django_select2.forms import Select2Widget
from entangled.forms import EntangledModelForm
from formset.collection import FormCollection
from formset.widgets import Selectize

from .models import Organization


class OrganizationForm(EntangledModelForm):
    class Meta:
        model = Organization
        fields = "__all__"
        # entangled_fields = {
        #     "data": ["name", "email_address", "established", "types", "links", "aliases", "acronyms", "labels"]
        # }


class OrganisationForm(forms.ModelForm):
    """Form for creating and updating organisations."""

    name = forms.ModelChoiceField(
        queryset=Organization.objects.all(), label=_("Organisation name"), required=False, widget=Selectize()
    )
    org_not_found = forms.BooleanField(label=_("I can't find my organisation!"), required=False)
    # ror_search = forms.Textarea(widget=ror.SearchWidget)

    ror_search = forms.CharField(
        label=_("Find an organisation using the ROR database"),
        required=False,
        widget=Select2Widget(
            attrs={
                "data-ajax--url": "https://api.ror.org/organizations?query={query}",
                "data-ajax--cache": "true",
                "data-ajax--delay": "250",
                "data-ajax--type": "GET",
                "data-ajax--dataType": "json",
                # "data-ajax--data": "function (params) { return { page: params.page || 1 }; }",
            }
        ),
    )

    class Meta:
        model = Organization
        fields = [
            "name",
            "org_not_found",
            "ror_search",
        ]


class OrganisationFormCollection(FormCollection):
    organisation = OrganisationForm()
    min_siblings = 1
    extra_siblings = 0
    # descriptions = DescriptionFormCollection(min_siblings=1, extra_siblings=1)

    # legend = _("Affiliations")
    add_label = _("Add new")
    related_field = "project"

    help_text = _("Add your affiliations.")

    def retrieve_instance(self, data):
        if data := data.get("dataset"):
            try:
                return self.instance.datasets.get(id=data.get("id") or 0)
            except (AttributeError, Organization.DoesNotExist, ValueError):
                return Organization(title=data.get("title"), project=self.instance)
