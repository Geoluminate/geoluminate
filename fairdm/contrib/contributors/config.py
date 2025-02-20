from django.utils.translation import gettext_lazy as _

import fairdm
from fairdm.metadata import Authority, Citation, ModelConfig

from .filters import ContributorFilter
from .models import Organization, Person


class FairDMCoreConfig(ModelConfig):
    authority = Authority(
        name=_("FairDM Core Development"),
        short_name="FairDM",
        website="https://fairdm.org",
    )
    citation = Citation(
        text="FairDM Core Development Team (2021). FairDM: A FAIR Data Management Tool. https://fairdm.org",
        doi="https://doi.org/10.5281/zenodo.123456",
    )
    repository_url = "https://github.com/FAIR-DM/fairdm"
    filterset_class = ContributorFilter


@fairdm.register(Person)
class PersonConfig(FairDMCoreConfig):
    # define project in terms of a scientific research project
    description = _(
        "A personal contributor to the creation of a research dataset is an individual who collects, organizes, and curates data for the study. This includes designing data collection methods, gathering information from various sources, and structuring the data for analysis. Their role is crucial in ensuring the dataset is comprehensive, accurate, and aligned with the research objectives."
    )


@fairdm.register(Organization)
class OrganizationConfig(FairDMCoreConfig):
    description = _(
        "An organizational contributor to a research dataset is an entity, such as a research institution, company, or nonprofit, that supports the creation, management, or distribution of the dataset. This can involve providing resources, funding, infrastructure, or access to data sources. Their role is key in facilitating the dataset's development, ensuring its accessibility, and often ensuring compliance with ethical and legal standards."
    )
