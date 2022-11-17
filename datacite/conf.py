"""Settings for Django CrossRef."""
from appconf import AppConf
from django.conf import settings

__all__ = ("settings", "DataCiteConf")

class DataCiteConf(AppConf):
    """Settings for Django DataCite"""

    DATACITE_DEFAULTS = {
    # These are default field values. The user cannot change these and they are hidden from the form.
    'resourceTypeGeneral': 'Dataset',
    'publisher': "GFZ Data Services",
    }

    DATACITE_RECOMMENDED = {
        # These are recommended field values. The user is still able to change these when filling out the form.
        'language': 'en',
        'license': 'CC BY 4.0',
    }

    class Meta:
        """Prefix for all Django DataCite settings."""
        prefix = "DATACITE"