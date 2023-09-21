from typing import Any, Dict, List, Optional, Type

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.db.models import CharField, F, Value
from django.db.models.functions import Concat
from django.db.models.query import QuerySet
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic import DetailView, ListView, TemplateView

from geoluminate.contrib.core.views.base import (
    BaseDetailView,
    CoreListView,
    HTMXMixin,
    ProjectBaseView,
)

from .menus import ContributorNav
from .models import Contributor


class ContributorListView(CoreListView):
    model = Contributor
    object_template = "contributor/contributor_object.html"


class ContributorDetailView(BaseDetailView):
    model = Contributor
    navigation = ContributorNav


class ContributorNetworkView(HTMXMixin, DetailView):
    template_name = "core/contributor_graph.html"
    model = Contributor

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


class BaseContributitionView(CoreListView):
    base_template = "user/base_list.html"
    model = Contributor

    def get_queryset(self):
        return self.object.datasets


# user_projects_view = BaseContributitionView.as_view(model=Project, extra_context={"can_create": True})
