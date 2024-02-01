from auto_datatables.views import AutoTableMixin
from django.apps import apps
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import resolve, reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView
from django.views.generic.edit import FormView as GenericFormView
from django.views.generic.edit import UpdateView
from django_filters.views import FilterView
from el_pagination.views import AjaxMultipleObjectTemplateResponseMixin
from formset.views import (
    FileUploadMixin,
    FormView,
    FormViewMixin,
    IncompleteSelectResponseMixin,
)
from meta.views import MetadataMixin


class DashboardRedirect(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse("contributor:detail", kwargs={"uuid": self.request.user.profile.uuid})


class HTMXMixin:
    base_template = None
    base_template_suffix = ".html"
    template_name = None
    object_list = None

    def get_base_template(self, **kwargs):
        # if getattr(self, "object_list"):
        # opts = self.object_list.model._meta
        # else:
        #     opts = self.model._meta
        if getattr(self, "model"):
            opts = self.model._meta
        else:
            opts = self.object_list.model._meta

        requesting_app_name = self.request.resolver_match.app_name
        names = [
            # f"{requesting_app_name}/base{self.base_template_suffix}",
            # f"{opts.app_label}/{opts.model_name}{self.base_template_suffix}",
            f"{opts.app_label}/base{self.base_template_suffix}",
            # f"{opts.app_label}/{opts.model_name}_base.html",
            f"base{self.base_template_suffix}",
            "base.html",
        ]
        print(self.base_template)
        if base_template := self.kwargs.get("base_template") or self.base_template:
            names.insert(0, base_template)
        print(names)
        return names

    def get_template_names(self):
        if self.request.htmx:
            return self.template_name
        return self.get_base_template()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["template_name"] = super().get_template_names()
        return context


@method_decorator(cache_page(60 * 5), name="dispatch")
class BaseListView(AjaxMultipleObjectTemplateResponseMixin, HTMXMixin, FilterView):
    base_template_suffix = "_list.html"
    object_template = None
    object_template_suffix = "_card.html"
    template_name = "geoluminate/base/list_view.html"
    page_template = "geoluminate/base/card_list.html"
    page_size = 20
    list_of = ""
    list_of_plural = ""
    header = ""
    columns: int = 1
    list_filter_top = ["title", "status", "o"]

    def get_filterset_class(self):
        """
        Returns the filterset class to use in this view
        """
        model = self.get_queryset().model
        model_name = model._meta.model_name
        app_config = apps.get_app_config(model._meta.app_label)
        if model_config := getattr(app_config, model_name, {}):
            self.filterset_class = model_config.get("filterset_class", self.filterset_class)
            self.filterset_fields = model_config.get("filterset_fields", self.filterset_fields)
        return super().get_filterset_class()

    def get_object_template(self, **kwargs):
        """Return the template name used for each object in the object_list for loop."""
        opts = self.object_list.model._meta
        return f"{opts.app_label}/{opts.model_name}{self.object_template_suffix}"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # the template to be used for displaying individual objects in the list
        context["object_template"] = self.object_template or self.get_object_template()
        context["list_of"] = self.list_of or self.object_list.model._meta.verbose_name_plural
        context["list_of_plural"] = self.list_of or self.object_list.model._meta.verbose_name_plural

        # normally, this is handled by the get method on el_pagination.views.AjaxListView but that conflicts with FilterView.
        context["page_template"] = self.page_template
        context["total_object_count"] = self.get_queryset().count()
        context["filtered_object_count"] = context["object_list"].count()
        context["can_create"] = self.kwargs.get("can_create", False)
        context["page_size"] = self.page_size
        context["is_filtered"] = hasattr(context["filter"].form, "cleaned_data")
        context["header"] = self.get_list_header()
        context["col"] = 12 // self.columns
        context["has_create_permission"] = self.has_create_permission()

        context["list_filter_top"] = self.list_filter_top

        return context

    def get_list_header(self):
        if self.header:
            return self.header
        x = self.list_of or self.object_list.model._meta.verbose_name_plural
        return f"GHFDB {x.title()}"

    def has_create_permission(self):
        """Returns True if the user has permission to add new objects."""
        return False


class BaseTableView(AutoTableMixin, TemplateView):
    filter = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = self.filter
        return context


class BaseDetailView(MetadataMixin, HTMXMixin, SingleObjectMixin):
    # base_template = "geoluminate/base/base_detail.html"
    base_template_suffix = "_detail.html"
    menu = []
    actions = []
    htmx = {
        # "target": "#contribPage",
    }
    allow_discussion = True

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        """Returns the profile object."""
        return self.model.objects.get(uuid=self.kwargs.get("uuid"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_menu"] = self.resolve_menu_urls()
        context["page_actions"] = self.resolve_action_urls()
        context["htmx"] = self.htmx
        context["has_edit_permission"] = self.has_edit_permission()
        context["allow_discussion"] = self.allow_discussion_section(obj=kwargs.get("object"))
        context["app_name"] = resolve(self.request.path_info).app_name
        context["edit_url"] = reverse(f"{context['app_name']}:edit", kwargs={"uuid": self.kwargs.get("uuid")})
        return context

    def has_edit_permission(self):
        return self.get_object().is_contributor(self.request.user)

    def resolve_menu_urls(self):
        """The menu item urls generated during the plugin registration process are not resolved until this method is called."""
        if not self.menu:
            raise NotImplementedError("You must define a menu attribute on the view.")
        for item in self.menu:
            item.resolved = reverse(item.url, kwargs={"uuid": self.kwargs.get("uuid")})
        return self.menu

    def resolve_action_urls(self):
        """The action item urls generated during the plugin registration process are not resolved until this method is called."""
        for item in self.actions:
            item.resolved = reverse(item.url, kwargs={"uuid": self.kwargs.get("uuid")})

        return self.actions

    def allow_discussion_section(self, obj=None):
        """Override this method to determine whether the discussion section should be displayed based on the current object."""
        return self.allow_discussion


# @method_decorator(cache_page(60 * 5), name="dispatch")
class BaseFormView(LoginRequiredMixin, HTMXMixin, UpdateView):
    slug_field = "uuid"
    slug_url_kwarg = "uuid"
    base_template = "geoluminate/base/create_view.html"
    template_name = "geoluminate/base/form_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # if self.object:
        # context["editing"] = True

        return context

    # def get_success_url(self):
    #     return self.object.get_absolute_url()
