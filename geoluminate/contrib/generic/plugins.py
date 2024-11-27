from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic import DetailView

from geoluminate import plugins
from geoluminate.contrib.generic.models import Description


@plugins.register(to=["project", "dataset", "sample"])
class Description(DetailView):
    model = Description
    name = _("About")
    title = _("About")
    icon = "overview"
    template_name = "plugins/about.html"

    def get_object(self):
        if hasattr(self, "object"):
            return self.object
        elif self.base_object:
            return self.base_object
        else:
            return super().get_object()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["descriptions"] = self.get_object().descriptions.all()
        context["all_types"] = self.object.DESCRIPTION_TYPES.choices
        context["config"] = {
            # "objects": list(self.object.dates.values("value", "type", "pk")),
            "date_types": self.object.DATE_TYPES.choices,
            "date_create_url": reverse("date-create", kwargs={"object_id": self.object.pk}),
            "description_types": self.object.DESCRIPTION_TYPES.choices,
            "description_create_url": reverse("description-create", kwargs={"object_id": self.object.pk}),
        }

        return context
