"""Contains settings for the following packages:

    - [django-rest-framework](https://www.django-rest-framework.org/api-guide/settings/)
    - [drf-spectacular](https://drf-spectacular.readthedocs.io/en/latest/settings.html#settings)
    - [drf-auto-endpoint](https://drf-auto-endpoint.readthedocs.io/en/latest/settings.html)
    - [django-cors-headers](https://github.com/adamchainz/django-cors-headers#setup)

All settings can be overridden in your project settings file.
"""

from django.utils.translation import gettext_lazy as _

# django-rest-framework - https://www.django-rest-framework.org/api-guide/settings/
REST_FRAMEWORK = {
    "HTML_SELECT_CUTOFF": 10,
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_THROTTLE_CLASSES": [
        "fairdm.contrib.api.throttling.AnonBurstRate",
        "fairdm.contrib.api.throttling.AnonSustainedRate",
        "fairdm.contrib.api.throttling.UserBurstRate",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon_burst": "4/second",
        "anon_sustained": "30/minute",
        "user_burst": "25/second",
    },
    "DEFAULT_PERMISSION_CLASSES": [
        "fairdm.contrib.api.access_policies.CoreAccessPolicy",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.BrowsableAPIRenderer",
        "drf_orjson_renderer.renderers.ORJSONRenderer",
        # "rest_framework.renderers.TemplateHTMLRenderer",
        # "rest_framework_csv.renderers.PaginatedCSVRenderer",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
    "PAGE_SIZE": 100,
    "DEFAULT_PARSER_CLASSES": [
        "drf_orjson_renderer.parsers.ORJSONParser",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    # "DEFAULT_SCHEMA_CLASS": "fairdm.contrib.api.utils.CustomSchema",
    "DEFAULT_METADATA_CLASS": "drf_auto_endpoint.metadata.AutoMetadata",
    # "URL_FIELD_NAME": "details",
    # "DATETIME_FORMAT": "%Y-%m-%dT, %H:%M:%S",
}


# By Default swagger ui is available only to admin user(s). You can change permission classes to change that
# See more configuration options at https://drf-spectacular.readthedocs.io/en/latest/settings.html#settings
SPECTACULAR_SETTINGS = {
    "SCHEMA_PATH_PREFIX": "/api/",
    "SCHEMA_COERCE_PATH_PK_SUFFIX": True,
    "TITLE": _("API Documentation"),
    # "TOS": render_to_string("fairdm/pages/api/tos.html"),
    "TOS": "/api/tos/",
    # "CONTACT": {
    #     "name": GEOLUMINATE["governance"]["name"],
    #     "url": GEOLUMINATE["governance"]["url"],
    #     "email": "",
    # },
    "LICENSE": {
        "name": "CC BY 4.0",
        "url": "https://creativecommons.org/licenses/by/4.0/",
    },
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SERVE_PUBLIC": False,
    "SORT_OPERATIONS": False,
    "SORT_OPERATION_PARAMETERS": False,
    "SERVE_PERMISSIONS": ["rest_framework.permissions.IsAuthenticatedOrReadOnly"],
    # OTHER SETTINGS
    # 'AUTHENTICATION_WHITELIST': ['rest_framework.authentication.BasicAuthentication',],
    "PARSER_WHITELIST": [],
    "RENDERER_WHITELIST": [
        "drf_orjson_renderer.renderers.ORJSONRenderer",
    ],
    # Tools that generate code samples can use SERVERS to point to the correct domain
    "SERVERS": [
        {
            # "url": GEOLUMINATE["application"]["domain"],
            "description": "Production server",
        }
    ],
    # 'ENUM_NAME_OVERRIDES': {
    #     "TCorrTop/TCorrBot": "database.choices.TempCorrectionMethod",
    #     "TMethodTop/TMethodBot": "database.choices.TempMethod",
    #     },
    # "TAGS": GEOLUMINATE["database"]["keywords"],
    # Tags defined in the global scope
    "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,
        # "filter": True,
        # "defaultModelRendering": "model",
        "persistAuthorization": True,
        "requestSnippetsEnabled": True,
        "displayOperationId": False,
        "supportedSubmitMethods": ["get"],
        "displayRequestDuration": True,
        "tryItOutEnabled": False,
        "docExpansion": "none",
    },
    "PREPROCESSING_HOOKS": ["fairdm.contrib.api.utils.public_api"],
}  # type: ignore[var-annotated]

# django-cors-headers - https://github.com/adamchainz/django-cors-headers#setup
CORS_URLS_REGEX = r"^/api/.*$"


SPECTACULAR_SETTINGS["SERVERS"] = []  # F405
