from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.providers.orcid.provider import extract_from_dict
from django.conf import settings
from django.contrib import messages
from django.http import HttpRequest

from fairdm.contrib.contributors.models import ContributorIdentifier

from .choices import PersonalIdentifiers


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request: HttpRequest, sociallogin):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)

    def pre_social_login(self, request, sociallogin):
        """
        Override pre_social_login to process ORCID data before account creation.

        sociallogin: allauth.socialaccount.models.SocialLogin instance
        """
        if sociallogin.account.provider == "orcid":
            orcid_id = sociallogin.account.uid

            # Check if the orcid_id is already in the database. If it is, link the social account to the existing user
            if existing := ContributorIdentifier.objects.filter(value=orcid_id).first():
                sociallogin.user = existing.content_object

                # Set the user as active and save. Otherwise django-allauth will prevent login.
                # Users can exists in the database as inactive if they were added as a contributor to a project, dataset, etc.
                # without actually having an account.
                sociallogin.user.is_active = True
                sociallogin.user.save()
                messages.success(
                    request,
                    "We were able to match your ORCID account against existing information in our system and have updated your profile!",
                )

    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        user.identifiers.create(value=sociallogin.account.uid, type=PersonalIdentifiers.ORCID)
        return user

    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)

        user.name = extract_from_dict(data, ["person", "name", "credit-name", "value"])

        user.profile = extract_from_dict(data, ["person", "biography", "content"])

        other_names = extract_from_dict(data, ["person", "other-names", "other-name"])
        if other_names:
            user.alternative_names = [name["content"] for name in other_names]

        links = extract_from_dict(data, ["person", "researcher-urls", "researcher-url"])
        if links:
            user.links = [{"display": link["url-name"], "url": link["url"]["value"]} for link in links]
        return user
