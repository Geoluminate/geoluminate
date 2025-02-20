"""FairDM allows you to lockdown your entire site with a password or restrict access to staff or superusers only. To enable this feature, you must set one of the following environment variables:

LOCKDOWN_PASSWORDS: A list of passwords that users can use to access the site.
LOCKDOWN_STAFF_ONLY: A boolean that restricts access to staff users only.
LOCKDOWN_SUPERUSERS_ONLY: A boolean that restricts access to superusers only.

"""

env = globals()["env"]

LOCKDOWN_ENABLED = any(
    [
        env("LOCKDOWN_PASSWORDS"),
        env("LOCKDOWN_STAFF_ONLY"),
        env("LOCKDOWN_SUPERUSERS_ONLY"),
    ]
)

if any(
    [
        env("LOCKDOWN_STAFF_ONLY"),
        env("LOCKDOWN_SUPERUSERS_ONLY"),
    ]
):
    LOCKDOWN_FORM = "lockdown.forms.AuthForm"

LOCKDOWN_AUTHFORM_STAFF_ONLY = env("LOCKDOWN_STAFF_ONLY")

LOCKDOWN_AUTHFORM_SUPERUSERS_ONLY = env("LOCKDOWN_SUPERUSERS_ONLY")
