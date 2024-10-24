from django.utils.translation import gettext as _
from django.views.generic.base import TemplateView


class ActivityStream(TemplateView):
    name = _("Activity")
    title = _("Recent Activity")
    icon = "activity.svg"
    template_name = "core/plugins/activity_stream.html"


class Discussion(TemplateView):
    title = name = _("Discussion")
    icon = "comments.svg"
    template_name = "core/plugins/discussion.html"


class Images(TemplateView):
    name = _("Images")
    icon = "images.svg"
    template_name = "core/plugins/images.html"
    # queryset = Photo.objects.all()
    # filterset_class = PhotoFilter
