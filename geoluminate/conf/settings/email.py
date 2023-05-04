import environ

env = environ.Env()

# SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
# """"""

# EMAIL_HOST = "smtp.sendgrid.net"
# """"""
# EMAIL_HOST_USER = "apikey"  # this is exactly the value 'apikey'
# """"""
# EMAIL_HOST_PASSWORD = SENDGRID_API_KEY
# """"""
# EMAIL_PORT = 587
# """"""
# EMAIL_USE_TLS = True
# """"""

# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = env(
    "DJANGO_EMAIL_BACKEND",
    default="django.core.mail.backends.smtp.EmailBackend",
)

# https://docs.djangoproject.com/en/dev/ref/settings/#email-timeout
EMAIL_TIMEOUT = 5
""""""
