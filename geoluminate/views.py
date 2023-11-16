from auto_datatables.views import AutoTableMixin
from django.apps import apps
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView
from django_filters.views import FilterView
from el_pagination.views import AjaxMultipleObjectTemplateResponseMixin
from formset.views import FormView
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


class BaseListView(
    AjaxMultipleObjectTemplateResponseMixin,
    HTMXMixin,
    FilterView,
):
    base_template_suffix = "_list.html"
    object_template = None
    object_template_suffix = "_card.html"
    template_name = "geoluminate/base/list_view.html"
    page_template = "geoluminate/base/card_list.html"
    page_size = 20
    list_of = ""
    list_of_plural = ""

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
        return context


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


class BaseCreateView(LoginRequiredMixin, HTMXMixin, FormView, CreateView):
    base_template = "geoluminate/base/create_view.html"
    template_name = "geoluminate/base/form_view.html"

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        response = super().form_valid(form)
        # add the current user a contributor with the Project Leader and Contact Person roles
        if hasattr(self.object, "contributors"):
            self.object.contributors.create(profile=self.request.user.profile, roles="ProjectLeader,ContactPerson")
        return response

    def get_success_url(self):
        model_name = self.object._meta.model.__name__.lower()
        return reverse(f"{model_name}-edit", kwargs={"uuid": self.object.uuid})
