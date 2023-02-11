import os

LOCKDOWN_ENABLED = os.environ.get("DJANGO_ENV") == "staging"
""""""

LOCKDOWN_FORM = "lockdown.forms.AuthForm"
""""""

LOCKDOWN_AUTHFORM_STAFF_ONLY = True
""""""

LOCKDOWN_REMOTE_ADDR_EXCEPTIONS = ["127.0.0.1"]
""""""

LOCKDOWN_URL_EXCEPTIONS = [
    r"^/admin/",  # unlock admin urls
]
