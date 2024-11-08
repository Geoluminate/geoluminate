from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic import DetailView
from django.views.generic.base import TemplateView
from django_tables2 import SingleTableView

from geoluminate import plugins
from geoluminate.core.models import Description


class Overview(TemplateView):
    name = _("Overview")
    title = _("Overview")
    icon = "home.svg"
    template_name = "plugins/overview.html"
    sidebar_fields = []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sidebar_fields"] = self.sidebar_fields
        return context


@plugins.register(to=["project", "dataset", "sample"])
class Description(DetailView):
    model = Description
    name = _("About")
    title = _("About")
    icon = "overview.svg"
    template_name = "plugins/about.html"

    def get_object(self):
        if hasattr(self, "object"):
            return self.object
        elif hasattr(self, "base_object"):
            return self.base_object
        else:
            return super().get_object()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["descriptions"] = self.get_object().descriptions.all()
        context["all_types"] = self.object.DESCRIPTION_TYPES.choices
        context["dates_config"] = {
            # "objects": list(self.object.dates.values("value", "type", "pk")),
            "available_types": self.object.DATE_TYPES.choices,
            "create_url": reverse("date-create", kwargs={"base_pk": self.object.pk}),
        }

        context["description_config"] = {
            # "objects": list(self.object.descriptions.values("value", "type", "pk")),
            "available_types": self.object.DESCRIPTION_TYPES.choices,
            "create_url": reverse("description-create", kwargs={"base_pk": self.object.pk}),
        }
        return context


@plugins.register(to=["project", "dataset", "sample", "person", "organization"])
class ActivityStream(DetailView):
    name = _("Activity")
    title = _("Recent Activity")
    icon = "activity.svg"
    template_name = "plugins/activity_stream.html"

    def get_object(self):
        if hasattr(self, "object"):
            return self.object
        elif hasattr(self, "base_object"):
            return self.base_object
        else:
            return super().get_object()


@plugins.register(to=["project", "dataset", "sample", "person", "organization"])
class Discussion(TemplateView):
    title = name = _("Discussion")
    icon = "comments.svg"
    template_name = "plugins/discussion.html"


class Images(TemplateView):
    name = _("Images")
    icon = "images.svg"
    template_name = "plugins/images.html"


class TablePlugin(SingleTableView):
    template_name = "plugins/table.html"
