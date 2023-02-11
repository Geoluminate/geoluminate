import os

AUTH_USER_MODEL = "user.User"
""""""

# ACCOUNT_ADAPTER = 'user.adapter.AuthenticationAdapter'
# """"""

LOGIN_REDIRECT_URL = "/"
""""""

LOGIN_URL = "/accounts/login/"
""""""

ACCOUNT_USER_MODEL_USERNAME_FIELD = None
"""Users are identified by email instead of username"""

ACCOUNT_EMAIL_REQUIRED = True
""""""

ACCOUNT_USERNAME_REQUIRED = False
"""We don't use usernames so this is False"""


ACCOUNT_LOGOUT_ON_GET = True
"""Skip confirm logout screen"""

ACCOUNT_AUTHENTICATION_METHOD = "email"
"""Email authentication is mandatory"""

ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3
""""""
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
"""Email verification is mandatory"""

# After signing up
ACCOUNT_SIGNUP_REDIRECT_URL = "/"
""""""


# After clicking email confirmation link, user is logged in and redirected
# to home? page
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
""""""

ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
"""Log new user in after confirming email"""

ACCOUNT_MAX_EMAIL_ADDRESSES = 2
""""""

AUTHENTICATION_BACKENDS = ("allauth.account.auth_backends.AuthenticationBackend",)
""""""

ACCOUNT_FORMS = {
    "login": "geoluminate.contrib.user.forms.LoginForm",
    "signup": "geoluminate.contrib.user.forms.SignUpForm",
    "add_email": "geoluminate.contrib.user.forms.AddEmailForm",
    "change_password": "geoluminate.contrib.user.forms.ChangePasswordForm",
    "set_password": "geoluminate.contrib.user.forms.SetPasswordForm",
    "reset_password": "geoluminate.contrib.user.forms.ResetPasswordForm",
    "reset_password_from_key": "geoluminate.contrib.user.forms.ResetPasswordKeyForm",
    "disconnect": "allauth.socialaccount.forms.DisconnectForm",
}
""""""

SOCIALACCOUNT_FORMS = {
    "disconnect": "allauth.socialaccount.forms.DisconnectForm",
    "signup": "user.forms.SocialSignupForm",
}
""""""

SOCIALACCOUNT_AUTO_SIGNUP = False
""""""


SOCIALACCOUNT_PROVIDERS = {
    "orcid": {
        # Base domain of the API.
        "BASE_DOMAIN": "sandbox.orcid.org"
        if os.environ.get("DJANGO_ENV") == "development"
        else "orcid.org",
        # Member API or Public API?
        "MEMBER_API": False,
    }
}
""""""
