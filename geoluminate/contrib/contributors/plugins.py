from django.utils.translation import gettext as _
from django.views.generic import DetailView, UpdateView
from formset.views import FileUploadMixin, FormViewMixin

from geoluminate.contrib.core.plugins import ActivityStream
from geoluminate.contrib.datasets.views import DatasetListView
from geoluminate.contrib.projects.views import ProjectListView
from geoluminate.contrib.reviews.views import ReviewListView
from geoluminate.contrib.samples.views import BaseTableView, SampleTable
from geoluminate.plugins import contributor
from geoluminate.utils import icon

from .forms import UserProfileForm
from .models import Contributor
from .views import ContributorDetailView


@contributor.page("overview", icon="fa-solid fa-address-card")
class ContributorFormView(ContributorDetailView, FileUploadMixin, FormViewMixin, UpdateView):
    model = Contributor
    form_class = UserProfileForm
    template_name = "contributors/contributor_detail.html"
    # template_name = "contributors/contributor_form.html"
    success_url = "."

    def form_valid(self, form):
        if extra_data := self.get_extra_data():
            if extra_data.get("add") is True:
                form.instance.save()
        return super().form_valid(form)


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
        for obj in dataset_ids:
            ids = list(set([i["id"] for i in data if i["object_id"] == obj]))
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
class ContributorProjectsView(ContributorDetailView, ProjectListView):
    def get_queryset(self, *args, **kwargs):
        return self.get_object().projects.all()


@contributor.page("datasets", icon=icon("dataset"))
class ContributorDatasetsView(ContributorDetailView, DatasetListView):
    template_name = "datasets/dataset_list.html"

    def get_queryset(self, *args, **kwargs):
        # MAKE SURE THIS DISTINGUISHES BETWEEN PUBLIC AND PRIVATE DATASETS
        return self.get_object().datasets.all()


@contributor.page("samples", icon=icon("sample"))
class ContributorSamplesView(ContributorDetailView, BaseTableView):
    table = SampleTable
    template_name = "auto_datatables/base.html"


@contributor.page("reviews", icon=icon("review"))
class ContributorReviewsView(ContributorDetailView, ReviewListView):
    header = _("Your Reviews")
    template_name = "datasets/review_list.html"

    def get_queryset(self):
        return super().get_queryset().select_related("review").filter(review__reviewer=self.get_object().user)


@contributor.page("activity", icon=icon("activity"))
class ContributorActivityView(ContributorDetailView, ReviewListView):
    template_name = "geoluminate/plugins/activity_stream.html"
