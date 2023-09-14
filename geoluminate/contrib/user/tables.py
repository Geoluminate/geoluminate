from django.urls import reverse

from geoluminate.contrib.core.tables import DatasetTable, ProjectTable
from geoluminate.tables import ClientSideProcessing


class Projects(ProjectTable):
    config_class = ClientSideProcessing(buttons=[], dom="pt")
    layout_overrides = {}


class Datasets(DatasetTable):
    config_class = ClientSideProcessing(buttons=[], dom="pt")
    layout_overrides = {}
