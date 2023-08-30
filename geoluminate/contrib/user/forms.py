from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.forms.models import ModelForm
from django.utils.translation import gettext_lazy as _
from django_select2.forms import Select2Widget
from formset.collection import FormCollection
from formset.richtext.widgets import RichTextarea
from formset.widgets import (
    DateInput,
    DualSortableSelector,
    Selectize,
    UploadedFileInput,
)
from organizations.models import Organization

from geoluminate.contrib.project.choices import iso_639_1_languages

from .models import Profile


class BaseUserForm(ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["academic_title", "first_name", "last_name", "email"]


class ProfileFormNoImage(ModelForm):
    class Meta:
        model = Profile
        fields = ["name", "about", "lang"]

        widgets = {  # noqa: RUF012
            "about": RichTextarea,
        }


class UserProfileForm(ModelForm):
    lang = forms.ChoiceField(
        choices=iso_639_1_languages,
        initial="en",
        widget=Selectize(),
    )

    class Meta:
        model = Profile
        fields = [
            "lang",
            "name",
            "image",
            "about",
        ]

        widgets = {  # noqa: RUF012
            "image": UploadedFileInput,
            "about": RichTextarea,
        }


class UserForm(FormCollection):
    user = BaseUserForm()
    profile = UserProfileForm()


class UserAdminCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = get_user_model()
        fields = [
            "email",
            "password",
        ]


class UserAdminChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = (
            "email",
            "password",
        )


class SignupExtraForm(forms.ModelForm):
    """Form used by Django Allauth for collecting extra information during signup."""

    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = get_user_model()
        fields = (
            "first_name",
            "last_name",
        )

    def signup(self, request, user):
        """Save the user's first and last name."""
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.save()


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
