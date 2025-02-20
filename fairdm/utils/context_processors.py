import json

from django.conf import settings

from fairdm.contrib.identity.models import Authority, Database


def fairdm(request):
    # Get the current site
    # current_site = Site.objects.get_current()
    """A context processor that adds the following variables to the context:"""
    context = {
        "config": {
            "site_name": settings.SITE_NAME,
            "site_domain": settings.SITE_DOMAIN,
            "allow_registration": settings.ACCOUNT_ALLOW_REGISTRATION,
            # "site_domain": current_site.domain,
        },
        "identity": {
            "database": Database.get_solo(),
            "authority": Authority.get_solo(),
        },
        "features": settings.FEATURE_FLAGS,
    }
    context["json_config"] = json.dumps(context["config"])
    return context
