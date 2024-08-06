import mimetypes
import random
from pathlib import Path

import formset
from django.contrib.postgres.fields import ArrayField
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.files.base import ContentFile
from django.templatetags.static import static
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from formset.upload import depict_size, file_icon_url, get_thumbnail_path, split_mime_type
from imagekit.models import ProcessedImageField
from imagekit.processors import SmartResize
from polymorphic.models import PolymorphicModel
from research_vocabs.fields import TaggableConcepts

from geoluminate.contrib.core.models import AbstractIdentifier
from geoluminate.contrib.core.utils import inherited_choices_factory
from geoluminate.db import models

from . import choices

# from django.db.models.fields.files import FieldFile


def profile_image_path(instance, filename):
    """Return the path to the profile image for a contributor."""
    return f"contributors/{instance.pk}.webp"


THUMBNAIL_MAX_HEIGHT = 200
THUMBNAIL_MAX_WIDTH = 350


def thumbnail_image(storage, file_path, image_height=THUMBNAIL_MAX_HEIGHT):
    try:
        from PIL import Image, ImageOps

        image = Image.open(storage.open(file_path))
    except Exception as e:
        print(e)
        return staticfiles_storage.url("formset/icons/file-picture.svg")
    else:
        height = int(image_height)
        width = int(round(image.width * height / image.height))
        width, height = min(width, THUMBNAIL_MAX_WIDTH), min(height, THUMBNAIL_MAX_HEIGHT)
        thumb = ImageOps.fit(ImageOps.exif_transpose(image), (width, height))
        thumbnail_path = get_thumbnail_path(file_path, image_height)
        thumb_io = ContentFile(b"")
        thumb.save(thumb_io, format=image.format)
        thumb_io.seek(0)
        storage.save(thumbnail_path, thumb_io)
        return storage.url(thumbnail_path)


def get_file_info(field_file):
    if not field_file:
        return None
    file_path = Path(field_file.name)
    storage = field_file.storage
    content_type, _ = mimetypes.guess_type(file_path)
    mime_type, sub_type = split_mime_type(content_type)

    if mime_type == "image":
        if sub_type == "svg+xml":
            thumbnail_url = field_file.url
        else:
            thumbnail_path = get_thumbnail_path(file_path)
            if storage.exists(thumbnail_path):
                thumbnail_url = storage.url(thumbnail_path)
            else:
                thumbnail_url = thumbnail_image(storage, file_path)
    else:
        thumbnail_url = file_icon_url(mime_type, sub_type)

    if storage.exists(file_path):
        download_url = field_file.url
        file_size = depict_size(field_file.size)
    else:
        download_url = "javascript:void(0);"
        thumbnail_url = staticfiles_storage.url("formset/icons/file-missing.svg")
        file_size = "-"
    return {
        "content_type": content_type,
        "name": file_path.name,
        "path": field_file.name,
        "download_url": download_url,
        "thumbnail_url": thumbnail_url,
        "size": file_size,
    }


formset.upload.get_file_info = get_file_info
formset.upload.thumbnail_image = thumbnail_image


class Contributor(PolymorphicModel, models.Model):
    """A Contributor is a person or organisation that makes a contribution to a project, dataset, sample or measurement
    within the database. This model stores publicly available information about the contributor that can be used
    for proper attribution and formal publication of datasets. The fields are designed to align with the DataCite
    Contributor schema."""

    image = ProcessedImageField(
        verbose_name=_("profile image"),
        processors=[SmartResize(600, 600)],
        format="WEBP",
        options={"quality": 60},
        blank=True,
        null=True,
        upload_to=profile_image_path,
    )

    name = models.CharField(
        max_length=512,
        verbose_name=_("display name"),
        help_text=_("This name is displayed publicly within the website."),
    )

    alternative_names = ArrayField(
        base_field=models.CharField(max_length=512),
        verbose_name=_("alternative names"),
        help_text=_("Any other names by which the contributor is known."),
        blank=True,
        default=list,
    )

    about = models.TextField(null=True, blank=True)

    interests = TaggableConcepts(
        verbose_name=_("research interests"),
        help_text=_("A list of research interests for the contributor."),
        blank=True,
    )

    lang = models.CharField(
        max_length=255,
        verbose_name=_("language"),
        help_text=_("Language of the contributor."),
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ["name"]
        verbose_name = _("contributor")
        verbose_name_plural = _("contributors")

    def __str__(self):
        return self.name

    def default_affiliation(self):
        """Returns the default affiliation for the contributor. TODO: make this a foreign key to an organization model."""
        if self.user:
            return self.user.organizations_organization.first()
        return None

    def location(self):
        """Returns the location of the contributor. TODO: make this a foreign key to a location model."""
        return random.choice(["Potsdam", "Adelaide", "Dresden"])
        if self.user:
            return self.user.organization.location
        return None

    def get_absolute_url(self):
        return reverse("contributor-detail", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("contributor-update", kwargs={"pk": self.pk})

    def profile_image(self):
        if self.image:
            return self.image.url
        return static("img/brand/icon.svg")

    @property
    def type(self):
        if self.user:
            return _("Personal")
        return _("Organizational")

    @property
    def given(self):
        if self.user:
            return self.user.first_name
        return ""

    @property
    def family(self):
        if self.user:
            return self.user.last_name
        return ""

    @property
    def reviews(self):
        if self.user:
            return self.user.review_set.all()
        # return an empty Review queryset
        # return Review.objects.none()

    @cached_property
    def owner(self):
        return self.user or self.organization

    @property
    def preferred_email(self):
        if self.user:
            return self.user.email
        return self.organization.owner.user.email


class Identifier(AbstractIdentifier):
    IdentifierLookup = choices.IdentifierLookup
    PERS_ID_TYPES = choices.PersonalIdentifiers
    ORG_ID_TYPES = choices.OrganizationalIdentifiers
    SCHEME_CHOICES = inherited_choices_factory("ContributorIdentifiers", PERS_ID_TYPES, ORG_ID_TYPES)
    scheme = models.CharField(_("scheme"), max_length=32, choices=SCHEME_CHOICES)
    object = models.ForeignKey(to=Contributor, on_delete=models.CASCADE)
