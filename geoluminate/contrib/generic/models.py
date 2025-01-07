from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _

from geoluminate.db.fields import PartialDateField


class GenericModel(models.Model):
    """A model that can be used to store generic information."""

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=23)
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.type}: {self.value}"  # Display the type and a preview of the text

    def __repr__(self):
        return f"<{self}>"

    def get_update_url(self):
        return reverse(f"{self._meta.model_name}-update", kwargs={"pk": self.pk, "object_id": self.object_id})


class Description(GenericModel):
    type = models.CharField(max_length=50)
    value = models.TextField()

    class Meta:
        verbose_name = _("description")
        verbose_name_plural = _("descriptions")
        unique_together = ("content_type", "object_id", "type")


class Date(GenericModel):
    type = models.CharField(max_length=50)
    value = PartialDateField(_("date"))

    class Meta:
        verbose_name = _("date")
        verbose_name_plural = _("dates")
        unique_together = ("content_type", "object_id", "type")


class Identifier(GenericModel):
    type = models.CharField(max_length=50)
    value = models.CharField(_("identifier"), max_length=255, db_index=True, unique=True)

    class Meta:
        verbose_name = _("date")
        verbose_name_plural = _("dates")
        unique_together = ("content_type", "object_id", "type")

    # def __str__(self):
    #     return f"<{self.get_scheme_display()}: {self.identifier}>"

    # def URI(self):
    #     if url := self.IdentifierLookup.get(self.scheme):
    #         return f"{url}{self.identifier}"
