from client_side_image_cropping import ClientsideCroppingWidget
from django import forms
from django.forms.models import ModelForm
from django.utils.translation import gettext_lazy as _
from django_select2.forms import Select2MultipleWidget
from formset.widgets import Selectize, SelectizeMultiple, UploadedFileInput

from geoluminate.contrib.core.choices import iso_639_1_languages
from geoluminate.contrib.core.forms import ControlledMultipleTagField

from .models import Contribution, Contributor


class MultiTagForm(forms.Form):
    interests = ControlledMultipleTagField(
        choices=[
            (i, _(i)) for i in ["GIS", "Remote Sensing", "Geospatial Data Science", "Geospatial Data Engineering"]
        ],
        widget=SelectizeMultiple(),
    )

    status = ControlledMultipleTagField(
        choices=[
            (i, _(i))
            for i in [
                "Open to collaboration",
                "Looking for collaborators",
                "Busy",
                "Looking for work",
            ]
        ],
        widget=SelectizeMultiple(),
    )


# class ProfileOptions(EntangledModelForm):
#     can_contact = forms.BooleanField(
#         label=_("Can Contact"),
#         help_text=_("Allow other users to contact you through this site."),
#         required=False,
#     )

#     class Meta:
#         model = Contributor
#         entangled_fields = {"options": ["can_contact"]}


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
    interests = ControlledMultipleTagField(
        choices=[
            (i, _(i)) for i in ["GIS", "Remote Sensing", "Geospatial Data Science", "Geospatial Data Engineering"]
        ],
        widget=Select2MultipleWidget,
    )

    name = forms.CharField(help_text=_("Your name as it will appear on this site."))

    class Meta:
        model = Contributor
        fields = [
            "image",
            "name",
            "lang",
            "about",
            "interests",
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
        model = Contribution
        fields = [
            "profile",
            "roles",
        ]

        widgets = {
            "profile": Selectize(),
            "roles": SelectizeMultiple(),
        }
