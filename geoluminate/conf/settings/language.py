# https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = "en"
""""""


# https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True
""""""

USE_L10N = True
""""""


PARLER_DEFAULT_LANGUAGE_CODE = "en"

PARLER_LANGUAGES = {
    1: (
        {"code": "en", "fallbacks": ["fr", "de"]},  # English with fallback to French and German
        {"code": "fr"},  # French
        {"code": "de"},  # German
    ),
    "default": {
        "fallback": "en",  # Default fallback language
        "hide_untranslated": False,  # Show entries even if no translation exists
    },
}
