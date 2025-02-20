"""Authentication related settings including the following external packages:

    - [django-allauth](https://django-allauth.readthedocs.io/en/latest/configuration.html)

All settings can be overridden in your project settings file.
"""

env = globals()["env"]

DEBUG = env("DJANGO_DEBUG")


ACCOUNT_ALLOW_REGISTRATION = env("DJANGO_ALLOW_SIGNUP")

# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = [
    # https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]

# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# https://docs.djangoproject.com/en/dev/ref/settings/#auth-user-model
AUTH_USER_MODEL = "contributors.Person"
""""""

# https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
LOGIN_REDIRECT_URL = "/"
""""""

# https://docs.djangoproject.com/en/dev/ref/settings/#login-url
LOGIN_URL = "account_login"
""""""

ACCOUNT_USER_MODEL_USERNAME_FIELD = None
"""Users are identified by email instead of username"""

ACCOUNT_EMAIL_REQUIRED = True
""""""

ACCOUNT_USERNAME_REQUIRED = False
"""We don't use usernames so this is False"""


ACCOUNT_LOGOUT_ON_GET = True
"""Skip confirm logout screen"""

# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_AUTHENTICATION_METHOD = "email"
"""Email authentication is mandatory"""

ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3
""""""

ACCOUNT_EMAIL_VERIFICATION = "mandatory"
"""Email verification is mandatory"""

# After signing up
# ACCOUNT_SIGNUP_REDIRECT_URL = "/"
# """"""

# After clicking email confirmation link, user is logged in and redirected
# to home? page
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
""""""

ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
"""Log new user in after confirming email"""

ACCOUNT_MAX_EMAIL_ADDRESSES = 4
""""""

# https://docs.djangoproject.com/en/dev/ref/settings/#authentication-backends
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]
""""""

# https://django-allauth.readthedocs.io/en/latest/forms.html
# ACCOUNT_FORMS = {
#     "login": "fairdm.contrib.users.forms.LoginForm",
#     # "signup": "fairdm.contrib.users.forms.SignUpForm",
#     "add_email": "fairdm.contrib.users.forms.AddEmailForm",
#     "change_password": "fairdm.contrib.users.forms.ChangePasswordForm",
#     "set_password": "fairdm.contrib.users.forms.SetPasswordForm",
#     "reset_password": "fairdm.contrib.users.forms.ResetPasswordForm",
#     "reset_password_from_key": "fairdm.contrib.users.forms.ResetPasswordKeyForm",
#     "disconnect": "allauth.socialaccount.forms.DisconnectForm",
# }
# """"""

# SOCIALACCOUNT_FORMS = {
#     "disconnect": "allauth.socialaccount.forms.DisconnectForm",
#     "signup": "fairdm.contrib.users.forms.SocialSignupForm",
# }
# """"""

SOCIALACCOUNT_AUTO_SIGNUP = False
""""""

SOCIALACCOUNT_PROVIDERS = {
    "orcid": {
        "BASE_DOMAIN": "orcid.org" if not DEBUG else "sandbox.orcid.org",
        "MEMBER_API": False,
    }
}
""""""

# https://django-allauth.readthedocs.io/en/latest/configuration.html
SOCIALACCOUNT_ADAPTER = "fairdm.contrib.contributors.adapters.SocialAccountAdapter"


ACCOUNT_SIGNUP_FORM_CLASS = "fairdm.contrib.contributors.forms.person.SignupExtraForm"


# DJANGO-INVITATIONS SETTINGS
# https://django-invitations.readthedocs.io/en/latest/configuration.html

# ADAPTER FOR DJANGO-INVITATION TO USE DJANGO-ALLAUTH
ACCOUNT_ADAPTER = "invitations.models.InvitationsAdapter"
""""""

INVITATIONS_INVITATION_ONLY = True
""""""

# DJANGO-ORGANISATIONS SETTINGS
INVITATION_BACKEND = "organizations.backends.defaults.InvitationBackend"
""""""

REGISTRATION_BACKEND = "organizations.backends.defaults.RegistrationBackend"
""""""
