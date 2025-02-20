from django.utils.translation import gettext_lazy as _

import fairdm
from fairdm.metadata import Authority, Citation, ModelConfig

from .filters import DatasetFilter, ProjectFilter
from .forms import DatasetForm, ProjectForm
from .models import Dataset, Project


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


@fairdm.register(Project)
class ProjectConfig(FairDMCoreConfig):
    # define project in terms of a scientific research project
    description = _(
        "A project is an organized effort to investigate a specific question or problem, involving data collection and analysis. The project gathers raw data through various methods like surveys or experiments, which are then structured into datasets for further analysis. These datasets form the basis for drawing conclusions and generating knowledge in the field."
    )
    filterset_class = ProjectFilter
    form_class = ProjectForm


@fairdm.register(Dataset)
class DatasetConfig(FairDMCoreConfig):
    description = _(
        "A dataset is a collection of data organized for analysis, often gathered through specific data collection methods like surveys, experiments, or observations. It can include raw or processed data in various formats, structured or unstructured. The dataset serves as the foundation for drawing conclusions and supporting the research findings."
    )
    keywords = []
    filterset_class = DatasetFilter
    form_class = DatasetForm
