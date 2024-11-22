from django.utils.translation import gettext as _
from django.views.generic.base import TemplateView

from geoluminate import plugins


@plugins.register(to=["project", "dataset", "sample", "contributor"])
class Discussion(TemplateView):
    title = name = _("Discussion")
    icon = "comments"
    template_name = "plugins/discussion.html"


@plugins.register(to=["project", "dataset", "sample", "contributor"])
class ActivityStream(TemplateView):
    name = _("Activity")
    title = _("Recent Activity")
    icon = "activity"
    template_name = "plugins/activity_stream.html"


class Images(TemplateView):
    name = _("Images")
    icon = "images"
    template_name = "plugins/images.html"
