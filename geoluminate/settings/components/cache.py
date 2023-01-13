CACHES = {
    # … default cache config and others
    'default': {
        # "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    },
    "select2": {
        # "BACKEND": "django_redis.cache.RedisCache",
        # "LOCATION": "redis://127.0.0.1:6379/2",
        # "OPTIONS": {
        #     "CLIENT_CLASS": "django_redis.client.DefaultClient",
        # }
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        'LOCATION': 'select2',
    }
}

# Tell select2 which cache configuration to use:
SELECT2_CACHE_BACKEND = "select2"
