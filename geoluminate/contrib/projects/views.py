from django.conf import settings
from django.urls import reverse
from formset.views import EditCollectionView

from geoluminate.contrib.core.views import BaseDetailView, CoreListView

from .forms import ProjectFormCollection
from .models import Project


class ProjectListView(CoreListView):
    model = Project


class ProjectDetail(BaseDetailView):
    model = Project
    navigation = settings.GEOLUMINATE_PROJECT_PAGES


class AddProjectView(EditCollectionView):
    slug_field = "uuid"
    slug_url_kwarg = "uuid"
    model = Project
    collection_class = ProjectFormCollection
    template_name = "core/base_form_collection.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        if self.object:
            context_data["edit"] = True
        else:
            context_data["add"] = True
        return context_data

    def get_object(self, queryset=None):
        if self.kwargs.get("uuid"):
            return self.model.objects.get(uuid=self.kwargs["uuid"])
        return self.model()

    def get_success_url(self):
        model_name = self.object._meta.model.__name__.lower()
        return reverse(f"{model_name}-edit", kwargs={"uuid": self.object.uuid})


list_view = ProjectListView.as_view()
