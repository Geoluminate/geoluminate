# django-invitations.readthedocs.io/en/latest/configuration.html

# ADAPTER FOR DJANGO-INVITATION TO USE DJANGO-ALLAUTH
ACCOUNT_ADAPTER = "invitations.models.InvitationsAdapter"
""""""

# DJANGO-ORGANISATIONS SETTINGS
INVITATION_BACKEND = "organizations.backends.defaults.InvitationBackend"
""""""

REGISTRATION_BACKEND = "organizations.backends.defaults.RegistrationBackend"
""""""

INVITATIONS_INVITATION_ONLY = True
""""""
