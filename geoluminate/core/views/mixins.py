from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import ListView
from el_pagination.views import AjaxMultipleObjectTemplateResponseMixin

from geoluminate.core.utils import get_model_class


class BaseObjectMixin:
    base_object_url_kwarg = "base_pk"

    def get_base_object_class(self):
        return get_model_class(self.kwargs.get(self.base_object_url_kwarg))

    def get_base_object(self):
        self.base_object = get_object_or_404(
            self.get_base_object_class(), pk=self.kwargs.get(self.base_object_url_kwarg)
        )
        return self.base_object


class HTMXMixin:
    htmx_fragment = "plugin"

    def get_template_names(self, template_names=None):
        if template_names is None:
            template_names = super().get_template_names()
        if self.request.htmx:
            fragment = self.request.GET.get("fragment", self.htmx_fragment)
            template_names = [f"{t}#{fragment}" for t in template_names]
        return template_names


class ListMixin(AjaxMultipleObjectTemplateResponseMixin):
    page_size = 20
    base_template = "geoluminate/base/list_view.html"
    page_template = "geoluminate/base/list_view.html#card"
    object_template = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # the template to be used for displaying individual objects in the list
        context["object_template"] = self.get_object_template()
        # normally, this is handled by the get method on el_pagination.views.AjaxListView but that conflicts with FilterView.
        # context["page_template"] = self.page_template
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

        # if template := getattr(self, "object_template", None):
        #     templates.insert(0, template)

        # return templates


class ListFilterMixin(ListMixin):
    list_filter_top: list[str] = []

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


class ListPluginMixin(ListMixin, ListView):
    # template_name = "geoluminate/base/list_view.html#page"
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
