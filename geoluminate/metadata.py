from dataclasses import asdict, dataclass, field

from research_vocabs.core import Concept


@dataclass(frozen=True, kw_only=True)
class Authority:
    name: str
    """The name of the authority that created this metadata. This is required."""

    short_name: str = ""
    """The short name of the authority that created this metadata."""

    website: str = ""
    """The website of the authority that created this metadata."""


@dataclass(frozen=True, kw_only=True)
class Citation:
    text: str = ""
    """The citation for the data model."""

    doi: str = ""
    """The DOI for the citation."""


# probably call this Config or something
@dataclass(frozen=True, kw_only=True)
class Metadata:
    metadata_version: str = "1.0"

    primary_data_fields: list[str] = field(default_factory=list)
    """A list of the primary data fields in the model. This is required."""

    description: str
    """A detailed description of the data model. This is required."""

    authority: Authority
    """The authority that created this metadata. This is required."""

    keywords: list[Concept]
    """A list of controlled keywords that describe the data model."""

    repo_url: str = ""
    """The URL of the repository where the data model can be viewed."""

    citation: Citation | list[Citation] = field(default_factory=list)
    """The citation for the data model."""

    maintainer: str = ""
    """The name of the package maintainer of the data model."""

    maintainer_email: str = ""
    """The email address of the package maintainer of the data model."""

    analagous_to: list[str | Concept] = field(default_factory=list)

    filterset_class: str = ""
    """The name of the filterset class that filters the data model."""

    filterset_fields: list[str] = field(default_factory=list)
    """A list of fields that are used to filter the data model. Only applicable if filterset_class is not provided."""

    def as_dict(self):
        return asdict(self)
