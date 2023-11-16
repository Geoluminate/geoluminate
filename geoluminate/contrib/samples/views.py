from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from geoluminate.tables import ClientSideProcessing
from geoluminate.utils import icon
from geoluminate.views import BaseDetailView, BaseTableView

from .models import Location, Sample
from .tables import SampleTable

list_view = BaseTableView.as_view(table=SampleTable)


class SampleDetail(BaseDetailView):
    model = Sample

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["tables"] = {
        #     "samples": SampleTable(
        #         url=reverse("sample-list", kwargs={"dataset_uuid": self.object.uuid}),
        #         config_class=ClientSideProcessing(buttons=[], dom="pt"),
        #         layout_overrides={},
        #     ),
        # }
        return context


class LocationView(BaseDetailView):
    model = Location
