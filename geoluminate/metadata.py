class MetaBase:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if k.startswith("_"):
                continue

            setattr(self, k, v)

            if getattr(self, k, None) is None:
                msg = f"Invalid metadata option '{k}' specified on class"
                raise AttributeError(msg)
            # else:
            # setattr(self, k, v)


class Authority(MetaBase):
    name: str = ""
    """The name of the authority that created this metadata. This is required."""

    short_name: str = ""
    """The short name of the authority that created this metadata."""

    website: str = ""
    """The website of the authority that created this metadata."""


class Citation(MetaBase):
    text: str = ""
    """The citation for the data model."""

    doi: str = ""
    """The DOI for the citation."""


class MetadataOpts:
    metadata_version = "1.0"

    # model: models.Model = None
    """The model class to use for this metadata class. This is required."""

    primary_data_fields: list = []
    """A list of the primary data fields in the model. This is required."""

    primary_data_types: list = []
    """A list of data types associated with the primary data fields."""

    summary = ""
    """A brief summary of the data model. This is required."""

    description = ""
    """A detailed description of the data model. This is required."""

    authority = ""
    """The authority that created this metadata. This is required."""

    website = ""
    """The website of the authority that created this metadata."""

    keywords: list = []
    """A list of keywords that describe the data model."""

    repo_url: str = ""
    """The URL of the repository where the data model is stored."""

    citation: str = ""
    """The citation for the data model."""

    maintainer: str = ""
    """The name of the package maintainer of the data model."""

    maintainer_email: str = ""
    """The email address of the package maintainer of the data model."""

    # def __new__(cls, name, bases, attrs):
    #     for k, v in attrs.items():
    #         if k.startswith("_"):
    #             continue
    #         elif getattr(cls, k, None) is None:
    #             msg = f"Invalid metadata option '{k}' specified on class '{cls.__name__}'"
    #             raise AttributeError(msg)
    #         else:
    #             setattr(cls, k, v)

    # def get_primary_data_types(cls):
    #     """Returns a dictionary of the primary data fields and their types."""
    #     pass
    # return {field: cls.primary_data_types[field] for field in cls.primary_data_fields}


class Metadata(MetaBase):
    metadata_version = "1.0"

    # model: models.Model = None
    """The model class to use for this metadata class. This is required."""

    primary_data_fields: list = []
    """A list of the primary data fields in the model. This is required."""

    primary_data_types: list = []
    """A list of data types associated with the primary data fields."""

    summary = ""
    """A brief summary of the data model. This is required."""

    description = ""
    """A detailed description of the data model. This is required."""

    authority: Authority = None
    """The authority that created this metadata. This is required."""

    keywords: list = []
    """A list of keywords that describe the data model."""

    repo_url: str = ""
    """The URL of the repository where the data model is stored."""

    citation: Citation = None
    """The citation for the data model."""

    maintainer: str = ""
    """The name of the package maintainer of the data model."""

    maintainer_email: str = ""
    """The email address of the package maintainer of the data model."""
