import logging
import environ
logger = logging.getLogger(__name__)

env = environ.Env(
    CACHE=(bool, False),

)



# https://docs.djangoproject.com/en/dev/ref/settings/#caches
if env("CACHE"):
# if True:
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
        "collectfasta": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": env("REDIS_URL"),
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
                "IGNORE_EXCEPTIONS": True,
            },
        },
        "select2": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": env("REDIS_URL"),
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
                "IGNORE_EXCEPTIONS": True,
            },
        },
    }
else:
    logger.info("Using Dummy cache")
    print("Using Dummy cache")
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.dummy.DummyCache",
            "LOCATION": "",
        },
        "collectfasta": {
            "BACKEND": "django.core.cache.backends.dummy.DummyCache",
            "LOCATION": "",
        },
        "select2": {
            "BACKEND": "django.core.cache.backends.dummy.DummyCache",
            "LOCATION": "",
        }
    }

# Tell select2 which cache configuration to use:
SELECT2_CACHE_BACKEND = "select2"

COLLECTFASTA_CACHE = "collectfasta"

COLLECTFASTA_THREADS = 8
