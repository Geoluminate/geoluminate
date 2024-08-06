from django.db import models


class ContributionManager(models.QuerySet):
    def by_role(self, role):
        """Returns all contributions with the given role"""
        return self.filter(roles__contains=role)

    # def get_contact_persons(self):
    #     return self.filter(roles__contains=ContributionRoles.CONTACT_PERSON)

    # def lead_contributors(self):
    #     """Returns all project leads"""
    #     return self.filter(roles__contains=ContributionRoles.PROJECT_LEADER)

    # def funding_contributors(self):
    #     """Returns all project leads"""
    #     return self.filter(roles__contains=ContributionRoles.SPONSOR)
