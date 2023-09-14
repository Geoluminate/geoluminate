import os

import xmlschema
from django.apps import apps
from django.utils.translation import gettext_lazy as _

from .utils import text_choices_factory


class DataCiteSchema:
    """Class that provides helper methods for working with the enum fields in the
    DataCite schema.

    Use like:

        >>> choices = DataCiteSchema("path/to/datacite.xsd")
        >>> choices.get_choices_for("titleType")
        <class 'geoluminate.contrib.core.datacite.titleTypeChoices'>
        >>> choices.get_help_text_for("titleType")
        'The type of the title.

    Available enums are:

    - titleType
    - resourceType
    - relationType
    - contributorType
    - dateType
    - relatedIdentifierType
    - fundingReferenceType
    - descriptionType
    - nameType
    - numberType
    """

    def __init__(self, file):
        self.schema = self.load(file)
        self.enums = self.get_enum_types()

    def load(self, file):
        """Load a new XMLSchema file."""
        app_config = apps.get_app_config("core")
        schema_dir = os.path.join(app_config.path, "schema", "datacite", "4.4", "metadata.xsd")
        return xmlschema.XMLSchema(schema_dir)

    def get_enum_types(self):
        """Return a dict of enumeration types."""
        enum_types = {}
        for k, v in self.schema.types.as_dict().items():
            if getattr(v, "enumeration", False):
                enum_types[k] = v
        return enum_types

    def get_choices_for(self, name):
        """Return a TextChoices class for a given name."""
        return text_choices_factory(name, self.enums[name].enumeration)

    def get_help_text_for(self, name):
        """Return help text (documentation) for a given name."""
        return self.enums[name].annotation.documentation[0].text


# choices = DataCiteSchema("test")
# choices = DataCiteSchema(settings.DATACITE_SCHEMA_VERSION)
