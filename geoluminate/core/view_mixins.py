from functools import cached_property

from django.apps import apps
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.module_loading import import_string
from django.views.generic import ListView
from django_tables2.export.views import ExportMixin
from django_tables2.views import SingleTableMixin

from geoluminate.core.utils import get_model_class


class RelatedObjectMixin:
    """Mixin to fetch and add a related object to the context for views behind the detail view of core models.

    This mixin is primarily used in plugins but can be applied to other views where a related object needs to be
    fetched based on a URL parameter. The related object is retrieved using the URL parameter specified by
    `base_object_url_kwarg` (defaults to `base_pk`). The related object is then added to the context with additional
    useful information about the related model.

    Attributes:
        base_object_url_kwarg (str): The URL keyword argument used to retrieve the primary key of the related object.

    Methods:
        get_related_model():
            Retrieves the related model class based on the URL parameter.

        base_object:
            A cached property that fetches the related object based on the primary key in the URL. If the related model
            is polymorphic, it retrieves a non-polymorphic version of the object.

        get_context_data(**kwargs):
            Adds the related object and related model metadata to the context for rendering.

    Example:
        urlpatterns = [
            path("project/<str:base_pk>/samples/", SampleListView.as_view(), name="sample-list"),
        ]

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

        Returns:
            object: The related object retrieved based on the primary key.

        Raises:
            Http404: If the related object does not exist.
        """
        pk = self.kwargs.get(self.base_object_url_kwarg)
        self.related_class = self.get_related_model()
        # if hasattr(self.related_class, "polymorphic_model_marker"):
        # return get_object_or_404(self.related_class.objects.non_polymorphic(), pk=pk)
        return get_object_or_404(self.related_class, pk=pk)

    def get_context_data(self, **kwargs):
        """Add the related object and related model information to the context.

        Adds the `base_object` (related object), related model class, and model metadata to the context dictionary.

        Args:
            **kwargs: Additional context parameters passed by the parent class.

        Returns:
            dict: The updated context dictionary containing the related object and model information.
        """
        context = super().get_context_data(**kwargs)
        context["base_object"] = self.base_object
        context["base_model"] = self.related_class
        context["base_model_name"] = self.related_class._meta.verbose_name
        context["base_model_name_plural"] = self.related_class._meta.verbose_name_plural
        context[self.related_class._meta.model_name] = self.base_object
        return context


class HTMXMixin:
    htmx_fragment = "plugin"

    def get_template_names(self, template_names=None):
        if template_names is None:
            template_names = super().get_template_names()
        if self.request.htmx:
            fragment = self.request.GET.get("fragment", self.htmx_fragment)
            template_names = [f"{t}#{fragment}" for t in template_names]
        return template_names


class ListMixin:
    page_size = 20
    base_template = "geoluminate/object_list.html"
    page_template = "geoluminate/object_list.html#card"
    object_template = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # the template to be used for displaying individual objects in the list
        context["object_template"] = self.get_object_template()
        context["total_object_count"] = self.get_queryset().count()
        context["page_size"] = self.page_size

        return context

    def get_object_template(self):
        if self.object_template:
            return self.object_template
        if hasattr(self.model, "get_inheritance_chain"):
            inherited_models = self.model.get_inheritance_chain()
            model_opts = [m._meta for m in inherited_models]
            return [f"{opts.app_label}/{opts.model_name}/card.html" for opts in model_opts]

        opts = self.model._meta if self.model else self.object_list.model._meta

        return [
            f"{opts.app_label}/{opts.model_name}_card.html",
            f"{opts.model_name}_card.html",
        ]


class ListFilterMixin(ListMixin):
    def get_filterset_class(self):
        """
        Returns the filterset class to use in this view
        """
        model = self.get_queryset().model

        options = getattr(model, "Options", None)
        if options:
            self.filterset_class = getattr(options, "filterset_class", self.filterset_class)
            self.filterset_fields = getattr(options, "filterset_fields", self.filterset_fields)
        return super().get_filterset_class()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if context["object_list"] is not None:
            context["filtered_object_count"] = context["object_list"].count()
        context["is_filtered"] = hasattr(context["filter"].form, "cleaned_data")
        return context


class TableMixin(ExportMixin, SingleTableMixin):
    export_formats = ["csv", "xls", "xlsx", "json", "latex", "ods", "tsv", "yaml"]
    template_name_suffix = "_table"
    base_model = None
    paginate_by = 20
    filterset_fields = ["name"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type_choices"] = self.base_model.get_polymorphic_choices(pluralize_labels=True)
        context["type_choices_dict"] = dict(context["type_choices"])
        context["current_type"] = self.request.GET.get("type", self.base_model.get_polymorphic_choices()[0][0])
        context["current_label"] = context["type_choices_dict"][context["current_type"]]
        return context

    @cached_property
    def model(self):
        default = self.base_model.get_polymorphic_choices()[0][0]
        model_class = apps.get_model(self.request.GET.get("type", default))
        return model_class

    def get_filterset_class(self):
        if hasattr(self.model.Config, "filterset_class"):
            return import_string(self.model.Config.filterset_class)
        return super().get_filterset_class()

    def get_table_class(self):
        return import_string(self.model.Config.table_class)


class ListPluginMixin(ListMixin, ListView):
    template_name = "plugins/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_list"] = self.get_queryset()
        return context


class PolymorphicSubclassMixin:
    template_name = "geoluminate/base/polymorphic_subclass_list.html"
    list_url = "sample-list"
    detail_url = "sample-type-detail"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subclasses = self.model.get_subclasses()

        result = []
        for stype in subclasses:
            metadata = stype.get_metadata()
            metadata["detail_url"] = reverse(self.detail_url, kwargs={"subclass": stype._meta.model_name.lower()})
            metadata["list_url"] = reverse(self.list_url, kwargs={"subclass": stype._meta.model_name.lower()})
            result.append(metadata)

        context["subclasses"] = result
        return context


class PolymorphicSubclassBaseView:
    base_model = None

    def get_model(self):
        subclass = self.kwargs.get("subclass")
        subclasses = self.base_model.get_subclasses()

        model = next((kls for kls in subclasses if kls._meta.model_name.lower() == subclass), None)

        if model is None:
            raise Http404("Measurement type does not exist")
        return model

    def get_queryset(self):
        self.model = self.get_model()
        return self.model.objects.all()

    def get_meta_title(self, context):
        return self.model._meta.verbose_name_plural
