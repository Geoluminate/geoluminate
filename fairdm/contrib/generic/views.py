from actstream import action
from django.db.models.base import Model as Model
from django.shortcuts import redirect
from django.utils.translation import gettext as _
from django.views.generic.edit import UpdateView
from extra_views import ModelFormSetView, UpdateWithInlinesView

from fairdm.core.models import Dataset
from fairdm.registry import registry

# from .models import Date
# from fairdm.core.models.dataset import DatasetDate
from fairdm.utils.utils import get_core_object_or_404

from .forms import CoreFormset, DateForm, DescriptionInline, KeywordForm


class BaseFormsetView(ModelFormSetView):
    """
    A base view for handling model formsets with dynamic vocabulary integration.

    Behavior:
        - The formset is associated with a specific object determined via `get_object()`.
        - Vocabulary choices are dynamically injected into the context and formset.
        - On successful submission, the view redirects to the same page.
    """

    form_class = None
    formset_class = None
    template_name = None

    @property
    def model(self):
        return self.get_object().dates.model

    def get_object(self):
        return get_core_object_or_404(self.kwargs.get("pk"))

    def get_success_url(self):
        return self.request.path


class UpdateDatesView(BaseFormsetView):
    """
    A view for updating date-related milestones using a formset.

    Behavior:
        - Retrieves the related date records for the object.
        - Provides vocabulary choices based on the object's `DATE_TYPES`.
        - Logs an action when the formset is successfully submitted.
    """

    form_class = DateForm
    formset_class = CoreFormset
    template_name = "generic/milestone.html"

    def construct_formset(self):
        formset = super().construct_formset()
        formset.helper.form_id = "date-form-collection"
        return formset

    def get_formset_kwargs(self):
        kwargs = super().get_formset_kwargs()
        kwargs.update({"queryset": self.get_queryset()})
        return kwargs

    def get_queryset(self):
        return self.get_object().dates.all()

    def formset_valid(self, formset):
        response = super().formset_valid(formset)
        action.send(
            self.request.user,
            verb=_("updated"),
            target=self.get_object(),
            description=_("Updated milestones."),
        )

        return response


class UpdateKeywordsView(UpdateView):
    """Presents a form to update the keywords of a Project, Dataset, Sample or Measurment."""

    model = Dataset
    form_class = KeywordForm
    template_name = "generic/keywords.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_list"] = self.get_object().keywords.all()
        context["tags"] = self.get_object().tags.all()
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        return form

    def form_valid(self, form):
        super().form_valid(form)
        return redirect(self.request.path)

    def form_invalid(self, form):
        return super().form_invalid(form)


# class DatasetUpdateWithDescriptions(GenericInlineFormSetView):
#     model = Dataset
#     inline_model = Description
#     form_class = DescriptionForm
#     formset_class = DescriptionFormset
#     factory_kwargs = {
#         "can_delete": False,
#         "can_delete_extra": False,
#     }
#     formset_kwargs = {
#         "vocabulary": Dataset.DESCRIPTION_TYPES,
#     }
#     template_name = "generic/dataset.html"

#     def get_object(self):
#         return get_core_object_or_404(self.kwargs.get("pk"))

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         return context


class UpdateCoreObjectBasicInfo(UpdateWithInlinesView):
    """Presents a form to update the name and descriptions of a Project, Dataset, Sample or Measurment."""

    template_name = "generic/dataset.html"
    inlines = [DescriptionInline]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_object(self):
        obj = get_core_object_or_404(self.kwargs.get("pk"))
        self.model = obj.__class__
        return obj

    def get_form_class(self):
        """Return the form class to use."""
        return registry.get_model(self.model)["config"].get_form_class()
        # return self.model._fairdm.config.get_form_class()
        # return modelform_factory(
        #     self.model,
        #     form=import_string(self.model.Config.form_class),
        #     fields=flatten_fieldsets(self.model.Config.fieldsets),
        # )
