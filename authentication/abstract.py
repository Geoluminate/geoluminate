from django.contrib.auth.models import AbstractUser
from .managers import UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

class NoUsernameAbstractUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']

    objects = UserManager()

    class Meta:
        abstract=True

    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.username)

    def get_full_name(self):
        """This method is used by the comments framework as a display name"""
        return self.first_name

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def display_name(self):
        return f'{self.first_name[0]}.{self.last_name}'

    def initials(self):
        return f'{self.first_name[0]}{self.last_name[0]}'

    def first_l(self):
        return f'{self.first_name}{self.last_name[0].capitalize()}'

    @property
    def username(self):
        return self.display_name()