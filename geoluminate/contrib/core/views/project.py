from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import modelform_factory
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView

from ..filters import ProjectFilter
from ..forms import DatasetForm, ProjectForm, ProjectFormCollection
from ..models import Dataset, Project
from .base import CoreListView, ProjectBaseView


class ProjectListView(CoreListView):
    model = Project


list_view = ProjectListView.as_view()


class ProjectDetail(ProjectBaseView):
    model = Project
    collection_class = ProjectFormCollection

    panels = [
        {
            "title": _("About"),
            "template_name": "project/partials/about.html",
            "icon": "fas fa-circle-info",
        },
        dict(
            title=_("Contributors"),
            template_name="project/partials/contributors.html",
            icon="fas fa-users",
        ),
        dict(
            title=_("Timeline"),
            template_name="project/partials/timeline.html",
            icon="fas fa-timeline",
        ),
        dict(
            title=_("Map"),
            template_name="core/map.html",
            icon="fas fa-map-location-dot",
        ),
        dict(
            title="Datasets",
            template_name="core/project/dataset_list.html",
            icon="fas fa-folder-open",
        ),
        dict(
            title=_("Discussion"),
            template_name="geoluminate/components/comments.html",
            icon="fas fa-comments",
        ),
        dict(
            title=_("Attachments"),
            template_name="core/partials/attachments.html",
            icon="fas fa-paperclip",
        ),
    ]


detail_view = ProjectDetail.as_view()
detail_map_view = ProjectDetail.as_view(template_name="project/detail_map.html")


class ProjectEdit(LoginRequiredMixin, ProjectDetail):
    collection_class = ProjectFormCollection
    panels = [
        dict(
            title=_("About"),
            template_name="project/partials/about.html",
            icon="fas fa-circle-info",
        ),
        dict(
            title=_("Contributors"),
            template_name="project/partials/contributors.html",
            icon="fas fa-users",
        ),
        dict(
            title=_("Timeline"),
            template_name="project/partials/timeline.html",
            icon="fas fa-timeline",
        ),
        dict(
            title=_("Map"),
            template_name="geoluminate/components/map.html",
            icon="fas fa-map-location-dot",
        ),
        dict(
            title="Datasets",
            template_name="partials/dataset_list.html",
            icon="fas fa-folder-open",
            form=DatasetForm,
        ),
        dict(
            title=_("Discussion"),
            template_name="geoluminate/components/comments.html",
            icon="fas fa-comments",
        ),
        dict(
            title=_("Attachments"),
            template_name="geoluminate/components/comments.html",
            icon="fas fa-paperclip",
        ),
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object:
            context["edit"] = True
        else:
            context["add"] = True
        form = modelform_factory(model=Dataset, fields=["title", "project"])
        context["add_dataset_form"] = form(initial={"project": self.object})
        return context

    def form_valid(self, form):
        if extra_data := self.get_extra_data():
            if extra_data.get("add") is True:
                form.instance.save()
            if extra_data.get("delete") is True:
                form.instance.delete()
                return JsonResponse({"success_url": self.get_success_url()})
        return super().form_valid(form)

    def get_object(self, queryset=None):
        if not self.extra_context.get("add"):
            return super().get_object(queryset)

    # def form_valid(self, form):
    #     if extra_data := self.get_extra_data():
    #         if extra_data.get("delete") is True:
    #             self.object.delete()
    #             success_url = self.get_success_url()
    #             response_data = {"success_url": force_str(success_url)} if success_url else {}
    #             return JsonResponse(response_data)
    #     return super().form_valid(form)


crud_view = ProjectEdit.as_view

add_view = ProjectEdit.as_view(extra_context={"add": True})

edit_view = ProjectEdit.as_view(extra_context={"edit": True})

# class ProjectAdd(LoginRequiredMixin, ProjectEdit):
#     extra_context = {"add": True}
