from django.urls import include, path
from neapolitan.views import Role

from fairdm.menus import ProjectMenu
from fairdm.plugins import plugins
from fairdm.views import FairDMDetailView, FairDMListView

from .models import Dataset, Project
from .views import (
    DatasetCRUDView,
    DataTableView,
    ProjectCRUDView,
    SampleCRUDView,
)

# re_path(UUID_RE_PATTERN, DirectoryView.as_view(), name="directory"),

urlpatterns = [
    *ProjectCRUDView.get_urls(),
    path("projects/", FairDMListView.as_view(model=Project), name="project-list"),
    path("projects/<str:pk>/", FairDMDetailView.as_view(model=Project, menu=ProjectMenu), name="project-detail"),
    path("project/<str:pk>/", include(plugins.get_urls("project"))),
    *DatasetCRUDView.get_urls(),
    path("datasets/", FairDMListView.as_view(model=Dataset), name="dataset-list"),
    path("dataset/<str:pk>/", include(plugins.get_urls("dataset"))),
    *SampleCRUDView.get_urls(roles=[Role.CREATE, Role.DETAIL, Role.UPDATE, Role.DELETE]),
    path("sample/<str:pk>/", include(plugins.get_urls("sample"))),
    path("data/", DataTableView.as_view(), name="data-table"),
]
