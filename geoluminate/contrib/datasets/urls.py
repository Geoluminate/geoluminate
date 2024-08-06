from django.urls import include, path
from neapolitan.views import Role

from geoluminate.contrib.contributors.views import ContributionCRUDView
from geoluminate.contrib.samples.views import SampleEditView

from .models import Contribution
from .plugins import dataset
from .views import DatasetEditView, DatasetListView

urlpatterns = [
    path("datasets/", DatasetListView.as_view(), name="dataset-list"),
    *DatasetEditView.get_urls(),
    path(
        "d/<uuid:pk>/",
        include(
            [
                *dataset.urls,
                *ContributionCRUDView.get_urls(Contribution, roles=[Role.CREATE, Role.UPDATE, Role.DELETE]),
                *SampleEditView.get_urls(roles=[Role.CREATE]),
            ]
        ),
    ),
    # path("d/<uuid:pk>/", include(SampleEditView.get_urls(roles=[Role.CREATE])), kwargs={"related_name": Dataset}),
]
