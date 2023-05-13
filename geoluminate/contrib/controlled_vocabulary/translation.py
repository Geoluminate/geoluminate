from modeltranslation.translator import TranslationOptions, register

from .models import ControlledVocabulary


@register(ControlledVocabulary)
class NewsTranslationOptions(TranslationOptions):
    fields = ("name", "description")
