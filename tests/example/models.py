from django.db import models

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

    class Meta:
        verbose_name = "Test Data"
        verbose_name_plural = "Test Data"

        permissions = [
            ("geoluminate_database_admin", "Can access the geoluminate database admin"),
        ]
