from django.db import models

from geoluminate.contrib.controlled_vocabulary.fields import (
    ControlledVocab,
    ControlledVocabMulti,
)
from geoluminate.models import Geoluminate


class TestData(Geoluminate):
    """Test Data model for geoluminate"""

    some_field = models.CharField(
        verbose_name="Some Field",
        help_text="Some Field",
        max_length=255,
        blank=True,
        null=True,
    )
    vocab_single = ControlledVocab("test_vocab_single", on_delete=models.SET_NULL, blank=True, null=True)
    vocab_multi = ControlledVocabMulti("test_vocab_multi", blank=True)

    class Meta:
        verbose_name = "Test Data"
        verbose_name_plural = "Test Data"
