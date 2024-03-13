import environ

env = environ.Env(
    # set casting, default value
    LOCKDOWN_ENABLED=(bool, False),
    LOCKDOWN_STAFF_ONLY=(bool, True),
)

LOCKDOWN_ENABLED = env("LOCKDOWN_ENABLED")
""""""

LOCKDOWN_FORM = "lockdown.forms.AuthForm"
""""""

LOCKDOWN_AUTHFORM_STAFF_ONLY = env("LOCKDOWN_STAFF_ONLY")
""""""


