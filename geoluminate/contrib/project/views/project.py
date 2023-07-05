from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.views.generic import UpdateView
from django.views.generic.base import RedirectView
from django.views.generic.detail import DetailView
from formset.views import FileUploadMixin, FormViewMixin

from geoluminate.views import SmallTableView

from ..forms import ProjectForm
from ..models import Contributor, Project


class ProjectDataTable(SmallTableView):
    model = Project
    fields = ["id", "get_absolute_url_button", "name", "description", "get_status_display", "start_date", "end_date"]
    search_fields = ["title"]
    # filter_fields = ["status"]
    extra_attributes = {
        "get_status_display": {"title": _("Status")},
        "get_absolute_url_button": {"title": "", "orderable": "false"},
        "start_date": {"title": _("Start")},
        "end_date": {"title": _("End")},
    }


class ProjectEditView(FileUploadMixin, FormViewMixin, LoginRequiredMixin, UpdateView):
    model = Project
    template_name = "project/edit.html"
    form_class = ProjectForm
    # success_url = reverse_lazy('address-list')  # or whatever makes sense
    # extra_context = None

    def get_object(self, queryset=None):
        if self.extra_context["add"] is False:
            return super().get_object(queryset)

    def form_valid(self, form):
        if extra_data := self.get_extra_data():
            if extra_data.get("delete") is True:
                self.object.delete()
                success_url = self.get_success_url()
                response_data = {"success_url": force_str(success_url)} if success_url else {}
                return JsonResponse(response_data)
        return super().form_valid(form)


class ProjectDetailView(DetailView):
    model = Project
    template_name = "project/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["key_dates"] = self.get_key_dates(["start_date", "end_date"])
        context["contributors"] = Contributor.objects.filter(dataset__project=self.object).distinct()
        return context

    # function that will extract fields from self.model using a list of fields names
    def get_key_dates(self, fields):
        key_dates = []
        for field in fields:
            # f = self.model._meta.get_field(field)
            key_dates.append(
                {
                    "field": field,
                    "value": getattr(self.object, field),
                    "label": self.model._meta.get_field(field).verbose_name,
                }
            )
        return key_dates

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.prefetch_related("datasets", "datasets__samples")


# class view that accept a uuid and redirect to the project detail page based on a slug field on the same object
class ProjectRedirectView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        project = Project.objects.get(uuid=self.kwargs["uuid"])
        return project.get_absolute_url()
