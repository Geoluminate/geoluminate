AUTH_USER_MODEL = 'user.User'

ACCOUNT_ADAPTER = 'authentication.adapter.AuthenticationAdapter'

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
            'login': 'authentication.forms.LoginForm',
            'signup': 'authentication.forms.SignUpForm',
            'add_email': 'authentication.forms.AddEmailForm',
            'change_password': 'authentication.forms.ChangePasswordForm',
            'set_password': 'authentication.forms.SetPasswordForm',
            'reset_password': 'authentication.forms.ResetPasswordForm',
            'reset_password_from_key': 'authentication.forms.ResetPasswordKeyForm',
            'disconnect': 'allauth.socialaccount.forms.DisconnectForm',
        }

SOCIALACCOUNT_FORMS = {
    'disconnect': 'allauth.socialaccount.forms.DisconnectForm',
    'signup': 'authentication.forms.SocialSignupForm',
}