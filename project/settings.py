from geoluminate import settings
from geoluminate.settings import *

SITE_NAME = 'Geoluminate'

settings.INSTALLED_APPS.extend([
    # "debug_toolbar",
    # "template_profiler_panel",
])

settings.MIDDLEWARE.extend([
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
])
