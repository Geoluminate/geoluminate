import logging

logger = logging.getLogger(__name__)

cache = env.bool("CACHE", default=False)

# https://docs.djangoproject.com/en/dev/ref/settings/#caches
if cache:
    logger.info("Using Redis cache")
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": env("REDIS_URL"),
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
                # Mimicing memcache behavior.
                # https://github.com/jazzband/django-redis#memcached-exceptions-behavior
                "IGNORE_EXCEPTIONS": True,
            },
        },
    }
else:
    logger.info("Using Dummy cache")
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.dummy.DummyCache",
            "LOCATION": "",
        }
    }

# Tell select2 which cache configuration to use:
SELECT2_CACHE_BACKEND = "default"
