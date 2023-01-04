from polymorphic.models import PolymorphicModel
from .base import AbstractProject, AbstractContributor, AbstractDataset
from django.utils.translation import gettext_lazy as _


class Project(PolymorphicModel, AbstractProject):
    __doc__ = _(
        "Base model for all projects within your database.")


class Contributor(AbstractContributor):
    __doc__ = _(
        "Base model for contributors to projects within your database.")


class Dataset(AbstractDataset):
    __doc__ = _(
        "Base model for datasets to projects within your database.")
