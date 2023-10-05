from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.forms.models import ModelForm
from django.utils.translation import gettext_lazy as _
from formset.collection import FormCollection

from geoluminate.contrib.contributors.forms import UserProfileForm


class BaseUserForm(ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name", "email"]


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
