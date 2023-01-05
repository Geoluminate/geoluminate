from geoluminate import settings
from geoluminate.settings import *

settings.INSTALLED_APPS.extend([
    # "debug_toolbar",
    # "template_profiler_panel",
])

settings.MIDDLEWARE.extend([
    'debug_toolbar.middleware.DebugToolbarMiddleware',
])


CELERY_BROKER_URL = "redis://localhost:6379"
CELERY_RESULT_BACKEND = "redis://localhost:6379"
