env = globals()["env"]

# https://docs.djangoproject.com/en/dev/ref/settings/#caches
if env("DJANGO_CACHE"):
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
        },
    }

# Tell select2 which cache configuration to use:
SELECT2_CACHE_BACKEND = "select2"

COLLECTFASTA_CACHE = "collectfasta"

COLLECTFASTA_THREADS = 8

VOCABULARY_DEFAULT_CACHE = "default"
