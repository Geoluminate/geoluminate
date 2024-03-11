"""This page contains reusable plugins that don't require additional configuration beyond class attributes."""

from django.utils.translation import gettext as _

from geoluminate.utils import icon


class ActivityStream:
    name = _("Activity")
    icon = icon("activity")
    template_name = "geoluminate/plugins/activity_stream.html"


class Map:
    name = _("Explorer")
    icon = icon("map")
    template_name = "geoluminate/plugins/map.html"


class Discussion:
    name = _("Discussion")
    icon = icon("discussion")
    template_name = "geoluminate/plugins/discussion.html"
