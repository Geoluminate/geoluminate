from django import forms
from django.contrib.auth import get_user_model
from django.forms.models import ModelForm

User = get_user_model()


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


class BaseUserForm(ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name", "email"]


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]

    # def model_to_dict(self, contributor):
    #     try:
    #         return model_to_dict(contributor, fields=self._meta.fields, exclude=self._meta.exclude)
    #     except PersonalContributor.DoesNotExist:
    #         return {}

    # def construct_instance(self, contributor):
    #     try:
    #         profile = contributor
    #     except PersonalContributor.DoesNotExist:
    #         profile = PersonalContributor(user=user)
    #     form = ContributorForm(data=self.cleaned_data, instance=profile)
    #     if form.is_valid():
    #         construct_instance(form, profile)
    #         form.save()


# class CodeOfConductForm()
