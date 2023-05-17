from django.db import models
from django.db.models import Q


class ControlledVocabBase:
    def __init__(self, vocab_label, *args, **kwargs):
        """
        vocab_label: a list of vocabularies the user can chose terms from.
            The first entry of the list is the default vocabulary.
            An entry has one of the following format:
                'iso639-2': a vocabulary prefix
                'concept.Language': vocabulary concept
                '': any vocabulary
            Example: ['iso639-2', 'concept.language', '']
            'iso639-2' is the default voc on page load, but the user can
            also change to all vocabularies that have the concept = language,
            or any other vocabulary.

            vocab_label='myvoc' is syntactic sugar for ['myvoc']
        """
        kwargs["to"] = "controlled_vocabulary.ControlledVocabulary"
        kwargs["related_name"] = "+"
        kwargs["limit_choices_to"] = {"label": vocab_label}
        self.vocab_label = vocab_label

        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs["vocab_label"] = self.vocab_label
        return name, path, args, kwargs

    def choice_limiter(self):
        return Q(label=self.vocab_label)

    def get_choices_queryset(self):
        model = self.remote_field.model
        return model.objects.get(label=self.vocab_label).descendants()


class VocabularyField(ControlledVocabBase, models.ForeignKey):
    pass


class MultiVocabularyField(ControlledVocabBase, models.ManyToManyField):
    pass

    # def formfield(self, *args, **kwargs):
    #     """We use a different widget than the base class"""
    #     from django.contrib import admin

    #     kwargs["widget"] = ControlledTermWidget(
    #         self.remote_field, admin.site, self.vocabularies
    #     )
    #     return super().formfield(*args, **kwargs)
