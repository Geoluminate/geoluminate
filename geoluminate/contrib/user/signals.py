# When account is created via social, fire django-allauth signal to
# populate Django User record.
from allauth.account.signals import user_signed_up
from django.dispatch import receiver


@receiver(user_signed_up)
def user_signed_up_(request, user, sociallogin=None, **kwargs):
    """A
    When a social account is created successfully and this signal is received,
    django-allauth passes in the sociallogin param, giving access to metadata on the remote account, e.g.:
    """
    pass
    # if sociallogin:
    #     # Extract first / last names from social nets and store on User record
    #     if sociallogin.account.provider == 'twitter':
    #         name = sociallogin.account.extra_data['name']
    #         user.first_name = name.split()[0]
    #         user.last_name = name.split()[1]
    #     user.ORCID = sociallogin.account.uid
    #     user.ORCID_is_authenticated = True

    #     user.save()
