from functools import cached_property

from django.shortcuts import get_object_or_404
from meta.views import MetadataMixin

from fairdm.contrib.identity.models import Database
from fairdm.utils.utils import get_model_class


class FairDMBaseMixin(MetadataMixin):
    modals = []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["modals"] = self.get_modals()
        context["user_can_edit"] = self.user_can_edit()
        return context

    def get_modals(self):
        return self.modals

    def user_can_edit(self):
        return False

    def get_meta_title(self, context):
        return f"{Database.get_solo().safe_translation_getter('name')}"
        # return f"{} · {Database.get_solo().safe_translation_getter('name')}"


class RelatedObjectMixin:
    """Mixin to fetch and add a related object to the context for views behind the detail view of core models.

    This mixin is primarily used in plugins but can be applied to other views where a related object needs to be
    fetched based on a URL parameter. The related object is retrieved using the URL parameter specified by
    `base_object_url_kwarg` (defaults to `base_pk`). The related object is then added to the context with additional
    useful information about the related model.

    Example:
        class SampleListView(RelatedObjectMixin, ListView):
            def get_queryset(self):
                return self.base_object.samples.all()
    """

    base_object_url_kwarg = "base_pk"

    def get_related_model(self):
        """Retrieve the related model class.

        Uses the URL parameter specified by `base_object_url_kwarg` to fetch the related model class.

        Returns:
            model: The model class corresponding to the related object.
        """
        return get_model_class(self.kwargs.get(self.base_object_url_kwarg))

    @cached_property
    def base_object(self):
        """Fetch the related object based on the primary key in the URL.

        If the related model is polymorphic, the method fetches a non-polymorphic version of the object.
        """
        pk = self.kwargs.get(self.base_object_url_kwarg)
        self.related_class = self.get_related_model()
        return get_object_or_404(self.related_class, pk=pk)

    def get_context_data(self, **kwargs):
        """Add the related object and related model information to the context.

        Adds the `base_object` (related object), related model class, and model metadata to the context dictionary.
        """
        context = super().get_context_data(**kwargs)
        context["base_object"] = self.base_object
        context["base_model"] = self.related_class
        context[self.related_class._meta.model_name] = self.base_object
        return context


class HTMXMixin:
    """
    Modifies template selection to support HTMX requests by appending a fragment identifier.

    This mixin depends on `django-template-partials` and requires the correct fragment to be
    specified in the template for it to function properly.

    If the request is an HTMX request, the mixin retrieves the `fragment` parameter from the
    request's GET data (defaulting to `"plugin"`) and appends `#fragment` to each template name.
    This enables rendering specific template sections instead of full templates.

    When the request is not from HTMX, the mixin falls back to the standard template selection process.
    """

    htmx_fragment = "plugin"

    def get_template_names(self, template_names=None):
        if template_names is None:
            template_names = super().get_template_names()
        if self.request.htmx:
            fragment = self.request.GET.get("fragment", self.htmx_fragment)
            template_names = [f"{t}#{fragment}" for t in template_names]
        return template_names
