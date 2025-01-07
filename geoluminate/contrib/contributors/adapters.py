from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.providers.orcid.provider import extract_from_dict
from django.conf import settings
from django.http import HttpRequest

from .models import Person


class AccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request: HttpRequest):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)


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

            # 1. check if a user with this ORCID already exists
            # contributor is a geoluminate.contrib.contributors.models.Person instance
            contributor = Person.objects.filter(identifiers__value=orcid_id).first() or sociallogin.user

            # access the ORCID profile data and parse into our contributor model
            # NOTE: django_allauth has already populated the first_name, last_name, and email fields where available
            data = sociallogin.account.extra_data

            contributor.name = extract_from_dict(data, ["person", "name", "credit-name", "value"])

            contributor.profile = extract_from_dict(data, ["person", "biography", "content"])

            other_names = extract_from_dict(data, ["person", "other-names", "other-name"])
            if other_names:
                contributor.alternative_names = [name["content"] for name in other_names]

            links = extract_from_dict(data, ["person", "researcher-urls", "researcher-url"])
            if links:
                contributor.links = [{"display": link["url-name"], "url": link["url"]["value"]} for link in links]

            # contributor.save()

            # contributor.identifiers = extract_from_dict(data, ["person", "external-identifiers", "external-identifier"])

            # You can also validate or reject the login if needed
            # Raise an exception to stop the login process
            # raise Exception("Custom error message")
