from django import forms
from django.forms.models import ModelForm
from django.utils.translation import gettext_lazy as _
from formset.richtext.widgets import RichTextarea
from formset.widgets import Selectize, UploadedFileInput

from geoluminate.contrib.core.choices import iso_639_1_languages

from .models import Contributor


class ProfileFormNoImage(ModelForm):
    class Meta:
        model = Contributor
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
        model = Contributor
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
