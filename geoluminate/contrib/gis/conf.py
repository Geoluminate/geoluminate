"""Settings for Core GIS"""
from typing import List

from appconf import AppConf
from django.conf import settings

__all__ = ("settings", "CoreGIS")


class CoreGIS(AppConf):
    """Settings for Core GIS"""

    PLUGINS: List[str] = []
    """List of plugins for the Site model"""

    class Meta:
        """Prefix for all Django CrossRef settings."""

        prefix = "CORE_GIS"
