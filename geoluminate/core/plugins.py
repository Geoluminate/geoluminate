"""This page contains reusable plugins that don't require additional configuration beyond class attributes."""

from django.utils.translation import gettext as _

from geoluminate.core.utils import icon


class ActivityStream:
    name = _("Activity")
    title = _("Recent Activity")
    icon = icon("activity")
    template_name = "core/plugins/activity_stream.html"


class Map:
    name = _("Explorer")
    icon = icon("map")
    template_name = "core/plugins/map.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["map_source_list"] = {}
        return context

    def serialize_dataset_samples(self, dataset):
        return None


class Discussion:
    title = name = _("Discussion")
    icon = icon("discussion")
    template_name = "core/plugins/discussion.html"


class Images:
    name = _("Images")
    icon = icon("images")
    template_name = "core/plugins/images.html"
    # queryset = Photo.objects.all()
    # filterset_class = PhotoFilter
