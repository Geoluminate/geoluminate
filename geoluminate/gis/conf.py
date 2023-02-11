"""Settings for Core GIS"""
from django.conf import settings
from appconf import AppConf

__all__ = ("settings", "CoreGIS")


class CoreGIS(AppConf):
    """Settings for Core GIS"""

    PLUGINS = []
    """List of plugins for the Site model"""

    class Meta:
        """Prefix for all Django CrossRef settings."""
        prefix = "CORE_GIS"
