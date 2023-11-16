"""This page contains reusable plugins that don't require additional configuration beyond class attributes."""

from django.views.generic import TemplateView

from geoluminate.contrib.datasets.models import Dataset
from geoluminate.contrib.projects.models import Project
from geoluminate.contrib.projects.views import ProjectDetailView
from geoluminate.contrib.samples.models import Sample
from geoluminate.plugins import dataset, project, sample
from geoluminate.utils import icon
from geoluminate.views import BaseDetailView

# @project.page("map", icon=icon("map"), view_kwargs={"model": Project})
# @dataset.page("map", icon=icon("map"), view_kwargs={"model": Dataset})
# @sample.page("map", icon=icon("map"), view_kwargs={"model": Sample})
# class MapView(BaseDetailView, TemplateView):
#     template_name = "geoluminate/plugins/map.html"


# @project.page("discussion", icon=icon("discussion"), view_kwargs={"model": Project})
# @sample.page("discussion", icon=icon("discussion"), view_kwargs={"model": Sample})
# class DiscussionView(BaseDetailView, TemplateView):
#     template_name = "geoluminate/plugins/discussion.html"
