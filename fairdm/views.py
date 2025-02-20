from django.contrib.auth.decorators import login_required
from django.db.models.base import Model as Model
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views.generic import DetailView
from django_filters.views import FilterView
from neapolitan.views import CRUDView

from fairdm.contrib.contributors.utils import current_user_has_role
from fairdm.contrib.identity.models import Database
from fairdm.registry import registry
from fairdm.utils.view_mixins import FairDMBaseMixin, HTMXMixin


@method_decorator(login_required, name="show_form")
class BaseCRUDView(FairDMBaseMixin, HTMXMixin, CRUDView):
    ncols = 1
    menu = None
    path_converter = "str"
    paginate_by = 20
    modals = [
        "modals.social",
        "modals.milestones",
        "modals.keywords",
    ]

    def get_template_names(self):
        if self.template_name is not None:
            return [self.template_name]

        if self.model is not None and self.template_name_suffix is not None:
            return [
                f"{self.model._meta.app_label}/{self.model._meta.object_name.lower()}{self.template_name_suffix}.html",
                f"fairdm/object{self.template_name_suffix}.html",
            ]
        return super().get_template_names()

    def get_detail_context_data(self, context):
        context["user_can_edit"] = self.user_can_edit()
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menu"] = self.menu
        func_name = f"get_{self.role.value}_context_data"
        if hasattr(self, func_name):
            context = getattr(self, func_name)(context)
        return context

    def get_meta_title(self, context):
        value = context["object_verbose_name_plural"].capitalize()
        if self.role.value == "create":
            value = _(f"Create {self.model._meta.verbose_name}")
        if self.object:
            value = self.object
        if self.role.value == "edit":
            value = _(f"Edit {self.model._meta.verbose_name}")
        context["title"] = value
        return f"{value} · {Database.get_solo().safe_translation_getter('name')}"


# @method_decorator(cache_page(60 * 5), name="dispatch")
class FairDMListView(FairDMBaseMixin, FilterView):
    """
    The base class for displaying a list of objects within the FairDM framework.
    """

    template_name_suffix = "_list"
    ncols = 1
    object_template = None

    def get_model(self):
        return self.model or self.queryset.model

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if context["object_list"] is not None:
            context["filtered_object_count"] = context["object_list"].count()
        context["is_filtered"] = hasattr(context["filter"].form, "cleaned_data")
        context["object_template"] = self.get_object_template()
        context["object_verbose_name_plural"] = self.get_model()._meta.verbose_name_plural
        return context

    def get_filterset_class(self):
        config = registry.get_model(self.model)
        return config["config"].get_filterset_class()

    def get_object_template(self):
        """
        Determines the template(s) used to render individual objects in the list.

        - If `object_template` is explicitly set, it is returned as-is.
        - If the model has a `get_inheritance_chain()` method, it constructs template paths
          based on the inheritance hierarchy.
        - Otherwise, it generates a list of template paths based on the model's app label
          and name.

        Returns:
            str or list: A single template path or a list of possible template paths.
        """
        if hasattr(self.model, "get_inheritance_chain"):
            inherited_models = self.model.get_inheritance_chain()
            model_opts = [m._meta for m in inherited_models]
            return [f"{opts.app_label}/{opts.model_name}/card.html" for opts in model_opts]

        opts = self.model._meta if self.model else self.object_list.model._meta

        return [
            f"{opts.app_label}/{opts.model_name}_card.html",
            f"{opts.model_name}_card.html",
        ]

    def get_template_names(self):
        if self.template_name is not None:
            return [self.template_name]

        elif self.model is not None and self.template_name_suffix is not None:
            return [
                f"{self.model._meta.app_label}/{self.model._meta.object_name.lower()}{self.template_name_suffix}.html",
                f"fairdm/object{self.template_name_suffix}.html",
            ]

        return super().get_template_names()


class FairDMDetailView(FairDMBaseMixin, DetailView):
    model = None
    menu = None
    edit_roles = ["Creator", "Reviewer", "ProjectMember"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menu"] = self.menu
        return context

    def user_can_edit(self):
        if current_user_has_role(self.request, self.object, self.edit_roles):
            return True
        return super().user_can_edit()

    def get_meta_title(self, context):
        value = context["object"]
        context["title"] = value
        title = super().get_meta_title(context)
        return f"{value} · {title}"
