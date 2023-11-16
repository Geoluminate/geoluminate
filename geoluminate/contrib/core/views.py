from django.urls import reverse_lazy
from django.views.generic import DetailView
from formset.views import EditCollectionView, FormView

from geoluminate.views import HTMXMixin

from .forms import GenericDescriptionForm


class DescriptionFormView(DetailView, FormView):
    template_name = "core/description_form.html"
    form_class = GenericDescriptionForm
    success_url = "/"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # if getattr(self, "object", None):
        kwargs["content_object"] = self.get_object()
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class AddDescription(HTMXMixin, DescriptionFormView):
    base_template = "base_create_view.html"
    slug_field = "uuid"
    slug_url_kwarg = "uuid"


class EditDescription(HTMXMixin, EditCollectionView):
    base_template = "geoluminate/base/create_view.html"
    slug_field = "uuid"
    slug_url_kwarg = "uuid"
    template_name = "core/base_form_collection.html"
    success_url = reverse_lazy("dataset-list")

    def get_success_url(self):
        return self.request.path

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        if self.object:
            context_data["edit"] = True
            print("Edit")
        else:
            context_data["add"] = True
            print("Add")
        return context_data

    # def form_collection_valid(self, form_collection):

    #     with transaction.atomic():
    #         form_collection.construct_instance(self.object)
    #     # integrity errors may occur during construction, hence revalidate collection
    #     if form_collection.is_valid():
    #         print("Valid")
    #         return super().form_collection_valid(form_collection)
    #     else:
    #         pprint.pprint(form_collection.errors)
    #         return self.form_collection_invalid(form_collection)
