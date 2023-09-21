from django.db import models

from .choices import ContributionRoles


class ContributionManager(models.QuerySet):
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
