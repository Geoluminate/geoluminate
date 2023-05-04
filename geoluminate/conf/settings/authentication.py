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
AUTH_USER_MODEL = "user.User"
""""""

# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_ADAPTER = "geoluminate.contrib.user.adapters.AccountAdapter"
""""""

# https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
LOGIN_REDIRECT_URL = "users:redirect"
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

# https://docs.djangoproject.com/en/dev/ref/settings/#authentication-backends
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]
""""""

# https://django-allauth.readthedocs.io/en/latest/forms.html
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
        "BASE_DOMAIN": "orcid.org",
        "MEMBER_API": False,
    }
}
""""""

# https://django-allauth.readthedocs.io/en/latest/configuration.html
SOCIALACCOUNT_ADAPTER = "geoluminate.contrib.user.adapters.SocialAccountAdapter"
