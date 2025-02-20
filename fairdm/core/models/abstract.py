from django.db import models
from django.urls import reverse

# from rest_framework.authtoken.models import Token
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from easy_thumbnails.fields import ThumbnailerImageField
from model_utils import FieldTracker
from taggit.managers import TaggableManager

from fairdm.contrib.contributors.choices import IdentifierLookup
from fairdm.contrib.generic.models import TaggedItem
from fairdm.db.fields import PartialDateField
from fairdm.utils.utils import default_image_path


class BaseModel(models.Model):
    image = ThumbnailerImageField(
        verbose_name=_("image"),
        blank=True,
        null=True,
        upload_to=default_image_path,
    )
    name = models.CharField(_("name"), max_length=255)

    keywords = models.ManyToManyField(
        "research_vocabs.Concept",
        verbose_name=_("keywords"),
        help_text=_("Controlled keywords for enhanced discoverability"),
        blank=True,
    )
    tags = TaggableManager(through=TaggedItem, blank=True)

    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created",
        help_text="When this record was created.",
    )
    modified = models.DateTimeField(
        auto_now=True,
        verbose_name="Modified",
        help_text="When this record was last modified.",
    )

    options = models.JSONField(
        verbose_name=_("options"),
        null=True,
        blank=True,
    )

    tracker = FieldTracker()

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.name}"

    @property
    def title(self):
        return self.name

    def get_absolute_url(self):
        return reverse(f"{self._meta.model_name}-detail", kwargs={"pk": self.pk})

    def get_api_url(self):
        return reverse(f"api:{self._meta.model_name}-detail", kwargs={"pk": self.pk})

    def add_contributor(self, contributor, with_roles=None):
        """Adds a new contributor the object with the specified roles."""

        # if not with_roles:
        #     with_roles = ["Contributor"]

        contribution = self.contributors.create(contributor=contributor, roles=with_roles)
        return contribution

    def is_contributor(self, user):
        """Returns true if the user is a contributor."""

        return self.contributions.filter(contributor=user).exists()

    def get_descriptions_in_order(self):
        """Returns the descriptions in the correct order specified by the DESCRIPTION_TYPES vocabulary."""
        default_order = self.DESCRIPTION_TYPES.values
        descriptions = self.descriptions.all()
        return sorted(descriptions, key=lambda x: default_order.index(x.type))

    def get_dates_in_order(self):
        """Returns the dates in the correct order specified by the DATE_TYPES vocabulary."""
        default_order = self.DATE_TYPES.values
        dates = self.dates.all()
        return sorted(dates, key=lambda x: default_order.index(x.type))

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

    def verbose_name(self):
        return self._meta.verbose_name

    def verbose_name_plural(self):
        return self._meta.verbose_name_plural


class GenericModel(models.Model):
    """A model that can be used to store generic information."""

    VOCABULARY = None
    # FOR = None

    class Meta:
        abstract = True

    # def __new__(cls, *args, **kwargs):
    #     new_class = super().__new__(cls, *args, **kwargs)

    #     if new_class.VOCABULARY is not None:
    #         new_class.type.field.choices = cls.VOCABULARY.choices

    #     if new_class.FOR is not None:
    #         new_class.related = models.ForeignKey(cls.FOR, on_delete=models.CASCADE)

    #         # if not hasattr(cls._meta, "db_table") or cls._meta.db_table is None:
    #         new_class._meta.db_table = f"{cls.FOR._meta.db_table}_{cls.__name__.lower()}"

    #     return new_class

    def __init_subclass__(cls):
        if cls.VOCABULARY is not None:
            cls.type.field.choices = cls.VOCABULARY.choices

        # if cls.FOR is not None:
        #     # if not hasattr(cls._meta, "db_table") or cls._meta.db_table is None:
        #     cls._meta.db_table = f"{cls.FOR._meta.db_table}_{cls.__name__.lower()}"

        return super().__init_subclass__()

    def __str__(self):
        return f"{self.type}: {self.value}"  # Display the type and a preview of the text

    def __repr__(self):
        return f"<{self}>"

    def get_update_url(self):
        return reverse(f"{self._meta.model_name}-update", kwargs={"pk": self.pk, "object_id": self.object_id})

    def verbose_name(self):
        return self._meta.verbose_name

    def verbose_name_plural(self):
        return self._meta.verbose_name_plural


class AbstractDescription(GenericModel):
    type = models.CharField(max_length=50)
    value = models.TextField()

    class Meta:
        abstract = True
        verbose_name = _("description")
        verbose_name_plural = _("descriptions")
        default_related_name = "descriptions"


class AbstractDate(GenericModel):
    type = models.CharField(max_length=50)
    value = PartialDateField(_("date"))

    class Meta:
        abstract = True
        verbose_name = _("date")
        verbose_name_plural = _("dates")
        ordering = ["value"]
        default_related_name = "dates"


class AbstractIdentifier(GenericModel):
    type = models.CharField(max_length=50)
    value = models.CharField(_("identifier"), max_length=255, db_index=True, unique=True)

    class Meta:
        abstract = True
        verbose_name = _("identifier")
        verbose_name_plural = _("identifiers")
        default_related_name = "identifiers"

    def get_root_url(self):
        return IdentifierLookup.get(self.type)

    def get_absolute_url(self):
        value = func() if (func := getattr(self, f"slugify_{self.type.lower()}", None)) else self.value
        return f"{self.get_root_url()}{value}"

    def slugify_isni(self):
        return self.value.replace(" ", "")
