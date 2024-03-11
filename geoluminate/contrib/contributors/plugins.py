from django.db import models
from django.views.generic import DetailView, UpdateView
from formset.views import FileUploadMixin, FormViewMixin

from geoluminate.contrib.datasets.views import DatasetPlugin
from geoluminate.contrib.projects.views import ProjectPlugin
from geoluminate.contrib.reviews.views import ReviewListView, ReviewPlugin
from geoluminate.contrib.samples.views import BaseTableView, SampleTable
from geoluminate.plugins import PluginRegistry
from geoluminate.utils import icon

from .forms import UserProfileForm
from .models import Contributor
from .views import ContributorDetailView

contributor = PluginRegistry("contributor", base=ContributorDetailView)


@contributor.page("overview", icon=icon("overview"))
class ContributorOverview(ContributorDetailView, FileUploadMixin, FormViewMixin, UpdateView):
    model = Contributor
    form_class = UserProfileForm
    # template_name = "contributors/contributor_overview.html"
    template_name = "contributors/contributor_detail.html"

    def has_edit_permission(self):
        """TODO: Add permissions."""
        return self.get_object() == self.request.user.profile


class ContributorNetworkView(ContributorDetailView, DetailView):
    template_name = "core/contributor_graph.html"

    def get_associations(self):
        obj_ids = self.object.contributions.values_list("object_id", flat=True)

        return (
            self.model.filter(
                object_id__in=obj_ids,
            )
            .values("profile", "object_id")
            .annotate(id=models.F("profile__id"), label=models.F("profile__name"), image=models.F("profile__image"))
            .values("id", "label", "object_id", "image")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["contributors"] = self.get_contributors()
        related_contributions = self.object.get_related_contributions()
        data = (
            related_contributions.values("profile", "object_id")
            .annotate(id=models.F("profile__id"), label=models.F("profile__name"), image=models.F("profile__image"))
            .values("id", "label", "object_id", "image")
        )
        dataset_ids = self.object.contributions.values("object_id").distinct()
        context["nodes"] = self.get_nodes(data)
        context["edges"] = self.get_edges(data, dataset_ids)
        return context

    def get_nodes(self, qs):
        # media_url = Concat(Value(settings.MEDIA_URL), F("image"), output_field=CharField())

        # get unique contributors and count the number of times they appear in the queryset
        nodes_qs = qs.values("id", "label", "image").annotate(value=models.Count("id")).distinct()

        nodes = []
        for d in nodes_qs:
            if d["image"]:
                d["image"] = settings.MEDIA_URL + d["image"]
            nodes.append(d)
        return nodes

    def get_edges(self, qs, dataset_ids):
        edges = []
        data = []  # not sure what this is for
        for obj in dataset_ids:
            ids = list({i["id"] for i in data if i["object_id"] == obj})
            ids.sort()

            # get list of unique id pairs
            pairs = []
            for i in range(len(ids)):
                for j in range(i + 1, len(ids)):
                    pairs.append((ids[i], ids[j]))

            edges += pairs

        # count the number of times each pair appears in edges
        return [{"from": f, "to": t, "value": edges.count((f, t))} for f, t in set(edges)]


@contributor.page("projects", icon=icon("project"))
class ContributorProjectsView(ContributorDetailView, ProjectPlugin):
    pass


@contributor.page("datasets", icon=icon("dataset"))
class ContributorDatasetsView(ContributorDetailView, DatasetPlugin):
    pass


@contributor.page("samples", icon=icon("sample"))
class ContributorSamplesView(ContributorDetailView, BaseTableView):
    table = SampleTable
    template_name = "auto_datatables/base.html"


@contributor.page("reviews", icon=icon("review"))
class ContributorReviewsView(ContributorDetailView, ReviewPlugin):
    pass


@contributor.page("activity", icon=icon("activity"))
class ContributorActivityView(ContributorDetailView, ReviewListView):
    template_name = "geoluminate/plugins/activity_stream.html"
