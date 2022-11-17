from geoluminate.gis.conf import settings


def get_polygon_plugins():
    """Fetches user listed plugins for the Site model"""
    return getattr(settings, 'CORE_GIS_PLUGINS')
