import logging

from allauth.account.signals import user_signed_up
from django.dispatch import receiver

from geoluminate.contrib.contributors.models import Contributor

logger = logging.getLogger(__name__)


@receiver(user_signed_up)
def create_profile(request, user, **kwargs):
    """Find a matching contributor profile or create a new one"""

    # if the user signed up with orcid, it will be available on the user object
    # we can use it to see if a profile is already associated with the user
    if user.orcid:
        logger.info(f"Found a profile matching the provided ORCID for {user.username}")
        # TODO
        # 1. check identifiers table for a matching orcid
        # 2. if there is a match, find the associated profile and update it with the user
    else:
        # no orcid provided, create a new profile and associate it with the user
        pass
    profile, created = Contributor.objects.get_or_create(user=user, defaults={"name": user.get_full_name()})
    print(profile, created)
    if created:
        logger.info(f"Created new profile for {user.username}")
