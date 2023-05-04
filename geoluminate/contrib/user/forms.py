from allauth.account import forms as auth_forms
from allauth.socialaccount.forms import SignupForm as SocialSignUp
from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Column, Field, Layout, Row, Submit
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class UserAdminCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = get_user_model()
        fields = (
            "email",
            "password",
        )


class UserAdminChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = (
            "email",
            "password",
        )


class LoginForm(auth_forms.LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = "POST"
        self.helper.form_id = "loginForm"
        self.helper.form_action = reverse("account_login")
        self.helper.form_show_labels = True
        self.helper.layout = Layout(
            FloatingField("login", label="email"),
            FloatingField("password", label="password"),
            Field("remember", template="forms/checkbox.html"),
        )


class SignUpForm(auth_forms.SignupForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = get_user_model()
        fields = (
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_method = "POST"
        self.helper.form_action = reverse("account_signup")
        self.helper.form_id = "signupForm"
        self.helper.layout = Layout(
            Row(
                Column(FloatingField("first_name"), css_class="col-md-6"),
                Column(FloatingField("last_name"), css_class="col-md-6"),
            ),
            FloatingField("email"),
            FloatingField("password1"),
            FloatingField("password2"),
        )


class AddEmailForm(auth_forms.AddEmailForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_labels = False
        self.helper.form_method = "POST"
        self.helper.form_action = reverse("account_email")
        self.helper.form_id = "addEmailForm"
        self.helper.layout = Layout(
            FloatingField("email", placeholder=""),
            Submit("action_add", value="Submit", hidden=True),
        )


class ChangePasswordForm(auth_forms.ChangePasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_method = "POST"
        self.helper.form_action = reverse("account_change_password")
        self.helper.form_id = "ChangePasswordForm"
        self.helper.layout = Layout(
            HTML(f'<p class="mb-3">{_("Please confirm your current password:")}</p>'),
            FloatingField("oldpassword"),
            HTML(f'<p class="mb-3">{_("Your new password:")}</p>'),
            FloatingField("password1"),
            FloatingField("password2"),
        )


class ResetPasswordForm(auth_forms.ResetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_method = "POST"
        self.helper.form_action = reverse("account_reset_password")
        self.helper.form_id = "resetPasswordForm"
        self.helper.layout = Layout(
            FloatingField("email"),
        )


class ResetPasswordKeyForm(auth_forms.ResetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_method = "POST"
        self.helper.form_action = reverse("account_reset_password_from_key")
        self.helper.form_id = "ResetPasswordKeyForm"
        self.helper.layout = Layout(
            FloatingField("password1"),
            FloatingField("password2"),
        )


class SocialSignupForm(SocialSignUp):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
