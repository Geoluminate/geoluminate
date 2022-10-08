AUTH_USER_MODEL = 'user.User'

ACCOUNT_ADAPTER = 'user.adapter.AuthenticationAdapter'

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/accounts/login/'

# Using email instead of username as identifier
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True 
ACCOUNT_USERNAME_REQUIRED = False #using email os this is False


#skip confirm logout screen
ACCOUNT_LOGOUT_ON_GET = True

# Use mandatory email authentication
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3
ACCOUNT_EMAIL_VERIFICATION = 'mandatory' #email verification is REQUIRED

# After signing up
ACCOUNT_SIGNUP_REDIRECT_URL='/'


# After clicking email confirmation link, user is logged in and redirected to home? page
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True #log new user in after confirming email


ACCOUNT_MAX_EMAIL_ADDRESSES = 2
AUTHENTICATION_BACKENDS = (
    "allauth.account.auth_backends.AuthenticationBackend",
)

ACCOUNT_FORMS = {
            'login': 'user.forms.LoginForm',
            'signup': 'user.forms.SignUpForm',
            'add_email': 'user.forms.AddEmailForm',
            'change_password': 'user.forms.ChangePasswordForm',
            'set_password': 'user.forms.SetPasswordForm',
            'reset_password': 'user.forms.ResetPasswordForm',
            'reset_password_from_key': 'user.forms.ResetPasswordKeyForm',
            'disconnect': 'allauth.socialaccount.forms.DisconnectForm',
        }

SOCIALACCOUNT_FORMS = {
    'disconnect': 'allauth.socialaccount.forms.DisconnectForm',
    'signup': 'user.forms.SocialSignupForm',
}