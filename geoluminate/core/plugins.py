"""This page contains reusable plugins that don't require additional configuration beyond class attributes."""

from django.utils.translation import gettext as _


class ActivityStream:
    name = _("Activity")
    title = _("Recent Activity")
    icon = "activity.svg"
    template_name = "core/plugins/activity_stream.html"


class Discussion:
    title = name = _("Discussion")
    icon = "comments.svg"
    template_name = "core/plugins/discussion.html"


class Images:
    name = _("Images")
    icon = "images.svg"
    template_name = "core/plugins/images.html"
    # queryset = Photo.objects.all()
    # filterset_class = PhotoFilter
