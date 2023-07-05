from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.forms.models import ModelForm
from formset.collection import FormCollection

from .models import Profile


class BaseUserForm(ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["academic_title", "first_name", "last_name", "email"]


class UserProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ["name", "about", "lang"]


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
