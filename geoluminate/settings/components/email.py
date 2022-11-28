import os

SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
""""""

EMAIL_HOST = 'smtp.sendgrid.net'
""""""
EMAIL_HOST_USER = 'apikey'  # this is exactly the value 'apikey'
""""""
EMAIL_HOST_PASSWORD = SENDGRID_API_KEY
""""""
EMAIL_PORT = 587
""""""
EMAIL_USE_TLS = True
""""""

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
""""""

if os.getenv('DJANGO_ENV') == 'development':
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
