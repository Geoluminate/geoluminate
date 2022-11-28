from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from .managers import UserManager
from django.db import models
from invitations.base_invitation import AbstractBaseInvitation


class User(AbstractUser):

    objects = UserManager()

    username = None
    email = models.EmailField(_('email address'), unique=True)
    # organizations = models.ForeignKey("research_organizations:ResearchOrganization",
    #                                   verbose_name=_('Organizations'),
    #                                   on_delete=models.SET_NULL)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        if self.username:
            return str(self.username)
        return 'User'

    @property
    def username(self):
        return self.display_name()

    # def get_full_name(self):
    #     """This method is used by the comments framework as a display name"""
    #     return self.first_name

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def display_name(self):
        if self.first_name and self.last_name:
            return f'{self.first_name[0]}.{self.last_name}'

    def initials(self):
        return f'{self.first_name[0]}{self.last_name[0]}'

    def first_l(self):
        return f'{self.first_name}{self.last_name[0].capitalize()}'

    def get_provider(self, provider):
        qs = self.socialaccount_set.filter(provider=provider)
        return qs.get() if qs else None

    @property
    def orcid(self):
        return self.get_provider('orcid')


class Invitations(AbstractBaseInvitation):
    pass
