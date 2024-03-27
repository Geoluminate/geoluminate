from auto_datatables.views import AutoTableMixin
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import resolve, reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django_filters.views import FilterView

from geoluminate.contrib.core.view_mixins import (
    BaseMixin,
    GeoluminatePermissionMixin,
    HTMXMixin,
    ListFilterMixin,
)

GEOLUMINATE = settings.GEOLUMINATE


class DashboardRedirect(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse("contributor:detail", kwargs={"uuid": self.request.user.profile.uuid})


@method_decorator(cache_page(60 * 5), name="dispatch")
class BaseListView(BaseMixin, ListFilterMixin, HTMXMixin, FilterView):
    """
    The base class for displaying a list of objects within the Geoluminate framework.
    """

    list_filter_top = ["title", "status", "o"]


@method_decorator(cache_page(60 * 10), name="dispatch")
class BaseTableView(BaseMixin, AutoTableMixin, TemplateView):
    filter = None
    table_view_name = "sample-list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = self.filter
        context["endpoint"] = self.get_table().url
        return context

    def get_table_url(self):
        if self.table_view_name and self.kwargs.get("uuid"):
            model_name = self.model._meta.model_name
            return reverse(
                self.table_view_name,
                kwargs={f"{model_name}_uuid": self.kwargs.get("uuid")},
            )
        return super().get_table_url()


# SingleObjectMixin, View
class BaseDetailView(BaseMixin, HTMXMixin, GeoluminatePermissionMixin, DetailView):
    # base_template = "geoluminate/base/base_detail.html"
    base_template_suffix = "_detail.html"
    menu = []
    actions = []
    htmx = {
        # "hx-target": "#main-content",
        # "hx-replace-url": "true",
        "hx-push-url": "true",
    }
    allow_discussion = True
    sidebar_components = [
        "core/sidebar/basic_info.html",
        "core/sidebar/keywords.html",
        "core/sidebar/status.html",
        "core/sidebar/summary.html",
    ]

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.request.toolbar.edit_mode_active = self.has_edit_permission()
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
        context["sidebar_components"] = self.sidebar_components
        return context

    def has_edit_permission(self):
        # check if user is logged in
        if not self.request.user.is_authenticated:
            return False
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


class BaseFormView(BaseMixin, HTMXMixin, LoginRequiredMixin, GeoluminatePermissionMixin, UpdateView):
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
