from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

# from rest_framework.authtoken.models import Token
from django.urls import reverse
from django.utils.decorators import classonlymethod
from django.utils.encoding import force_str
from django.utils.functional import cached_property
from django.utils.translation import gettext as _
from polymorphic.showfields import ShowFieldType

from geoluminate.core.utils import get_inheritance_chain, get_subclasses
from geoluminate.db import models
from geoluminate.db.fields import PartialDateField


class Abstract(models.Model):
    """An abstract model that contains common fields and methods for both the Project and Dataset models."""

    class Meta:
        abstract = True
        ordering = ["-modified"]

    def __str__(self):
        return force_str(self.title)

    def is_contributor(self, user):
        """Returns true if the user is a contributor."""

        return self.contributions.filter(contributor=user).exists()

    def get_api_url(self):
        return reverse(f"{type(self).__name__.lower()}-detail", kwargs={"pk": self.pk})

    def get_abstract(self):
        """Returns the abstract description of the project."""
        try:
            return self.descriptions.get(type="Abstract")
        except self.DoesNotExist:
            return None

    def get_meta_description(self):
        abstract = self.get_abstract()
        if abstract:
            return abstract.description
        else:
            return None

    @cached_property
    def get_descriptions(self):
        descriptions = list(self.descriptions.all())
        # descriptions.sort(key=lambda x: self.DESCRIPTION_TYPES.values.index(x.type))
        return descriptions


class DescriptionQuerySet(models.QuerySet):
    def get_first(self):
        choices = self.model.type_vocab.values
        return self.filter(type=choices[0]).first()


class GenericModel(models.Model):
    """A model that can be used to store generic information."""

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=23)
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        abstract = True


class Description(GenericModel):
    type = models.CharField(max_length=50)
    value = models.TextField()

    class Meta:
        verbose_name = _("description")
        verbose_name_plural = _("descriptions")
        unique_together = ("content_type", "object_id", "type")

    def __str__(self):
        return f"{self.type}: {self.value[:50]}"  # Display the type and a preview of the text

    def get_update_url(self):
        return reverse("description-update", kwargs={"pk": self.pk, "base_pk": self.object_id})


class Date(GenericModel):
    type = models.CharField(max_length=50)
    value = PartialDateField(_("date"))

    class Meta:
        verbose_name = _("date")
        verbose_name_plural = _("dates")
        unique_together = ("content_type", "object_id", "type")

    def __str__(self):
        return f"{self.type}: {self.value}"  # Display the type and a preview of the text


class Identifier(GenericModel):
    type = models.CharField(max_length=50)
    value = models.CharField(_("identifier"), max_length=255, db_index=True)

    class Meta:
        verbose_name = _("date")
        verbose_name_plural = _("dates")
        unique_together = ("content_type", "object_id", "type")

    # def __str__(self):
    #     return f"<{self.get_scheme_display()}: {self.identifier}>"

    # def URI(self):
    #     if url := self.IdentifierLookup.get(self.scheme):
    #         return f"{url}{self.identifier}"


class PolymorphicMixin(ShowFieldType):
    @classonlymethod
    def get_subclasses(cls):
        return get_subclasses(cls)

    @classonlymethod
    def get_polymorphic_choices(cls, include_self=False):
        choices = []
        for subclass in cls.get_subclasses():
            opts = subclass._meta
            choices.append((f"{opts.app_label}.{opts.model_name}", opts.verbose_name))
        return choices

    def get_type(self):
        return {
            "class": self.__class__.__name__,
            "app_label": self._meta.app_label,
            "model_name": self._meta.model_name,
            "verbose_name": self._meta.verbose_name,
            "verbose_name_plural": self._meta.verbose_name_plural,
        }

    @classmethod
    def get_metadata(cls):
        metadata = {}

        # for k in inheritance:
        if cls._metadata is not None:
            metadata.update(**cls._metadata.as_dict())

        inheritance = [
            k.get_metadata() for k in cls.mro()[:0:-1] if issubclass(k, cls.base_class()) and k != cls.base_class()
        ]

        metadata.update(
            name=cls._meta.verbose_name,
            name_plural=cls._meta.verbose_name_plural,
            inheritance=inheritance,
        )

        return metadata

    @classonlymethod
    def get_inheritance_chain(cls):
        return get_inheritance_chain(cls, cls.base_class())
