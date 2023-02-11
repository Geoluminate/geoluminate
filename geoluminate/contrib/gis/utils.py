from geoluminate.contrib.gis.conf import settings


def get_polygon_plugins():
    """Fetches user listed plugins for the Site model"""
    return getattr(settings, "CORE_GIS_PLUGINS")


def get_default_site_model():
    return
