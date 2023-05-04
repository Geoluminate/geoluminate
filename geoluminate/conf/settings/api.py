"""Default API settings"""

# django-rest-framework - https://www.django-rest-framework.org/api-guide/settings/
REST_FRAMEWORK = {
    "HTML_SELECT_CUTOFF": 10,
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_THROTTLE_CLASSES": [
        "geoluminate.contrib.api.throttling.AnonBurstRate",
        "geoluminate.contrib.api.throttling.AnonSustainedRate",
        "geoluminate.contrib.api.throttling.UserBurstRate",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon_burst": "4/second",
        "anon_sustained": "30/minute",
        "user_burst": "25/second",
    },
    "DEFAULT_PERMISSION_CLASSES": [
        "geoluminate.contrib.api.access_policies.CoreAccessPolicy",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "drf_orjson_renderer.renderers.ORJSONRenderer",
        "geoluminate.contrib.api.renderers.GeoJSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
        # "rest_framework_csv.renderers.PaginatedCSVRenderer",
        # "datatables.renderers.DatatablesORJSONRenderer",
    ],
    # 'DEFAULT_FILTER_BACKENDS': (
    # ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 100,
    "DEFAULT_PARSER_CLASSES": [
        "drf_orjson_renderer.parsers.ORJSONParser",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_METADATA_CLASS": "drf_auto_endpoint.metadata.AutoMetadata",
    # 'DEFAULT_METADATA_CLASS': 'datatables.metadata.DatatablesAutoMetadata',
}

# By Default swagger ui is available only to admin user(s). You can change permission classes to change that
# See more configuration options at https://drf-spectacular.readthedocs.io/en/latest/settings.html#settings
SPECTACULAR_SETTINGS = {
    "SCHEMA_PATH_PREFIX": r"/api/v[0-9]",
    "TITLE": "World Heat Flow Database API",
    "DESCRIPTION": "Documentation for version 1.0 of the public API of the World Heat Flow Database Project.",
    "TOS": None,
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SERVE_PUBLIC": False,
    "SORT_OPERATIONS": False,
    "SORT_OPERATION_PARAMETERS": False,
    "SERVE_PERMISSIONS": ["rest_framework.permissions.IsAdminUser"],
    # OTHER SETTINGS
    # 'AUTHENTICATION_WHITELIST': ['rest_framework.authentication.BasicAuthentication',],
    "PARSER_WHITELIST": [],
    # 'RENDERER_WHITELIST': [
    #     'drf_orjson_renderer.renderers.ORJSONRenderer',
    #     # 'rest_framework_csv.renderers.PaginatedCSVRenderer',
    #     ],
    "SERVERS": [],
    # 'ENUM_NAME_OVERRIDES': {
    #     "TCorrTop/TCorrBot": "database.choices.TempCorrectionMethod",
    #     "TMethodTop/TMethodBot": "database.choices.TempMethod",
    #     },
    "TAGS": [],
    # Tags defined in the global scope
    "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,
        "persistAuthorization": True,
        "displayOperationId": True,
        "supportedSubmitMethods": ["get"],
        "displayRequestDuration": True,
        "tryItOutEnabled": False,
    },
    "PREPROCESSING_HOOKS": ["geoluminate.core.datatables.spectacular.preprocessing_filter_spec"],
}  # type: ignore[var-annotated]
""""""

# django-cors-headers - https://github.com/adamchainz/django-cors-headers#setup
CORS_URLS_REGEX = r"^/api/.*$"
