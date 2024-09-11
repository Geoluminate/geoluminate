LANGUAGE_CODE = "en"

USE_I18N = True

USE_L10N = True

PARLER_DEFAULT_LANGUAGE_CODE = "en"

PARLER_LANGUAGES = {
    1: (
        {"code": "en"},
        {"code": "fr"},
        {"code": "de"},
    ),
    "default": {
        "fallback": "en",  # Default fallback language
        "hide_untranslated": False,  # Show entries even if no translation exists
    },
}
