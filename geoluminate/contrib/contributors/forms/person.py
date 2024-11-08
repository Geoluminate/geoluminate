from client_side_image_cropping import ClientsideCroppingWidget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Column, Layout, Row, Submit
from django import forms
from django.contrib.auth import get_user_model
from django.forms.models import ModelForm
from django.utils.translation import gettext as _

from geoluminate.core.choices import iso_639_1_languages

User = get_user_model()


class SignupExtraForm(forms.ModelForm):
    """Form used by Django Allauth for collecting extra information during signup."""

    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name")

    def signup(self, request, user):
        """Save the user's first and last name."""
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.save()


class BaseUserForm(ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name", "email"]


class UserProfileForm(forms.ModelForm):
    image = forms.ImageField(
        widget=ClientsideCroppingWidget(
            width=300,
            height=300,
            preview_width="100%",
            preview_height="100%",
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

    # hopefully this can be removed when this issue is solved: https://github.com/koendewit/django-client-side-image-cropping/issues/15
    class Media:
        css = {
            "all": (
                "client_side_image_cropping/croppie.css",
                # "client_side_image_cropping/cropping_widget.css",
            ),
        }
        js = (
            "client_side_image_cropping/croppie.min.js",
            "client_side_image_cropping/cropping_widget.js",
        )

    class Meta:
        model = User
        fields = "__all__"
        fields = ["image", "lang", "first_name", "last_name", "email", "name"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("name", "first_name", "last_name", css_class="col-md-8"),
                Column("image"),
                css_class="gx-5",
            ),
            "lang",
            "email",
            ButtonHolder(Submit("submit", "Save")),
        )


# class CodeOfConductForm()
