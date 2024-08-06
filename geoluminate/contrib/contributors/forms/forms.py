from client_side_image_cropping import ClientsideCroppingWidget
from crispy_forms.helper import FormHelper
from django import forms
from django.forms.models import ModelForm
from django.utils.translation import gettext as _
from django_select2.forms import Select2MultipleWidget, Select2Widget
from formset.widgets import Selectize, UploadedFileInput

from geoluminate.contrib.core.choices import iso_639_1_languages

from ..models import Contributor, Identifier


class UserProfileForm(ModelForm):
    image = forms.ImageField(
        widget=ClientsideCroppingWidget(
            width=300,
            height=300,
            preview_width=150,
            preview_height=150,
            file_name="profile.jpg",
        ),
        required=False,
        label=False,
    )
    lang = forms.ChoiceField(
        choices=iso_639_1_languages,
        initial="en",
        # widget=Selectize(),
        help_text=_("Preferred display language for this site (where possible)."),
        label=_("Language"),
    )

    name = forms.CharField(help_text=_("Your name as it will appear on this site."))

    class Meta:
        model = Contributor
        fields = [
            "image",
            "name",
            "lang",
            "about",
        ]


class AddContributorForm(ModelForm):
    """A form that can be used by a user to add details for a new contributor."""

    lang = forms.ChoiceField(
        choices=iso_639_1_languages,
        initial="en",
        widget=Selectize(),
    )

    class Meta:
        model = Contributor
        fields = [
            "image",
            "name",
            "lang",
            "about",
        ]

        widgets = {
            "image": UploadedFileInput,
            # "about": RichTextarea,
        }

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data["interests"] += cleaned_data["status"]
        return cleaned_data


class ContributionForm(ModelForm):
    """Used to modify contributors on a project, dataset, etc. and assign roles."""

    class Meta:
        # model = Contribution
        fields = [
            "object",
            "contributor",
            "roles",
        ]
        widgets = {
            "contributor": Select2Widget(),
            "roles": Select2MultipleWidget,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "contribution-form"
        # self.helper.include_media = False

    # def is_valid(self):
    #     is_valid = super().is_valid()
    #     print(self.errors)
    #     return is_valid


class ContributorForm(ModelForm):
    image = forms.ImageField(
        widget=UploadedFileInput(
            attrs={
                "max-size": 1024 * 1024,
            }
        ),
        help_text="Please do not upload files larger than 1MB",
        required=False,
    )

    class Meta:
        model = Contributor
        fields = ["image", "name", "about", "lang"]


class IdentifierForm(ModelForm):
    min_siblings = 0

    id = forms.IntegerField(required=False, widget=forms.HiddenInput)
    scheme = forms.ChoiceField(
        label=_("Scheme"),
        help_text=_("The scheme that the identifier is based on."),
        choices=[],  # set dynamically in __init__,
    )

    class Meta:
        model = Identifier
        fields = ["scheme", "identifier"]

    def __init__(self, scheme_choices, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["scheme"].choices = scheme_choices
