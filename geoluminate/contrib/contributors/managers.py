from django.db import models

from .choices import ContributionRoles


class ContributorManager(models.QuerySet):
    def active(self):
        """Returns all contributors where either user.is_active is True or organization manager is not Null"""
        return self.filter(models.Q(user__is_active=True) | models.Q(organization__owner__isnull=False))

    def persons(self):
        """Returns all personal contributors"""
        return self.filter(user__isnull=False)

    def organizations(self):
        """Returns all organizations"""
        return self.filter(organization__isnull=False)


class PersonManager(models.Manager):
    def get_queryset(self):
        return ContributorManager(self.model, using=self._db).persons()


class OrganizationManager(models.Manager):
    def get_queryset(self):
        return ContributorManager(self.model, using=self._db).organizations()


class ContributionManager(models.QuerySet):
    def by_role(self, role):
        """Returns all contributions with the given role"""
        return self.filter(roles__contains=role)

    def get_contact_persons(self):
        return self.filter(roles__contains=ContributionRoles.CONTACT_PERSON)

    def lead_contributors(self):
        """Returns all project leads"""
        return self.filter(roles__contains=ContributionRoles.PROJECT_LEADER)

    def funding_contributors(self):
        """Returns all project leads"""
        return self.filter(roles__contains=ContributionRoles.SPONSOR)

    def projects(self):
        """Returns all projects"""
        return self.filter(content_type__model="project")

    def datasets(self):
        """Returns all datasets"""
        return self.filter(content_type__model="dataset")

    def samples(self):
        """Returns all samples"""
        return self.filter(content_type__model="sample")
