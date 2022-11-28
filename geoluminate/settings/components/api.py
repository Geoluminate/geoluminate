"""Default API settings"""

# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': [
#         'rest_framework.authentication.BasicAuthentication',
#         'rest_framework.authentication.SessionAuthentication',
#    ],
#     'DEFAULT_RENDERER_CLASSES': [
#         'drf_ujson.renderers.UJSONRenderer',
#         # 'rest_framework.renderers.JSONRenderer',
#         'rest_framework.renderers.BrowsableAPIRenderer',
#         'drf_excel.renderers.XLSXRenderer',
#     ],
#     'DEFAULT_PARSER_CLASSES': [
#         'drf_ujson.parsers.UJSONParser',
#     ],
#     'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
#     'PAGE_SIZE': 100
# }


SPECTACULAR_SETTINGS = {
    'SCHEMA_PATH_PREFIX': r'/api/v[0-9]',
    'TITLE': 'World Heat Flow Database API',
    'DESCRIPTION': 'Documentation for version 1.0 of the public API of the World Heat Flow Database Project.',
    'TOS': None,
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SERVE_PUBLIC': False,
    'SORT_OPERATIONS': False,
    'SORT_OPERATION_PARAMETERS': False,
    # OTHER SETTINGS
    # 'AUTHENTICATION_WHITELIST': ['rest_framework.authentication.BasicAuthentication',],
    'PARSER_WHITELIST': [],
    # 'RENDERER_WHITELIST': [
    #     'drf_orjson_renderer.renderers.ORJSONRenderer',
    #     # 'rest_framework_csv.renderers.PaginatedCSVRenderer',
    #     ],
    'SERVERS': [],
    # 'ENUM_NAME_OVERRIDES': {
    #     "TCorrTop/TCorrBot": "database.choices.TempCorrectionMethod",
    #     "TMethodTop/TMethodBot": "database.choices.TempMethod",
    #     },
    'TAGS': [],
    # Tags defined in the global scope
    "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,
        "persistAuthorization": True,
        "displayOperationId": True,
        "supportedSubmitMethods": ['get'],
        "displayRequestDuration": True,
        "tryItOutEnabled": False,
    },
    "PREPROCESSING_HOOKS": [
        "datatables.spectacular.preprocessing_filter_spec"
    ],
}
""""""
