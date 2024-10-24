from actstream import actions
from django.apps import apps
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from django.forms import modelform_factory
from django.http import Http404
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from django.views.generic.edit import CreateView
from django_contact_form.views import ContactFormView

from ..forms import DescriptionForm


def follow_unfollow(request, content_type_id, object_id, flag=None, do_follow=True, actor_only=True):
    """This is a rewrite of the follow_unfollow view from django-activity-stream. The view now returns a html snippet for async HTMX updates of the follow button."""

    if not request.htmx:
        raise Http404

    ctype = get_object_or_404(ContentType, pk=content_type_id)
    instance = get_object_or_404(ctype.model_class(), pk=object_id)

    # If flag was omitted in url, None will pass to flag keyword argument
    flag = flag or ""

    if do_follow:
        actions.follow(request.user, instance, actor_only=actor_only, flag=flag)
    else:
        actions.unfollow(request.user, instance, flag=flag)
    return render(request, "core/follow_button.html", {"object": instance, "do_follow": do_follow})


@login_required
def update_object(request, content_type_id, object_id):
    """An experimental view that accepts a 'fields' parameter in the url and returns a form for updating the specified fields of the object."""

    # if not request.htmx:
    # raise Http404

    # get 'fields' parameter from url
    fields = request.GET.get("fields", "__all__")
    # print(fields)
    # if not fields:
    #     raise Http404("No fields parameter in url.")

    ctype = get_object_or_404(ContentType, pk=content_type_id)

    model_class = ctype.model_class()

    instance = get_object_or_404(model_class, pk=object_id)

    form_class = modelform_factory(model_class, fields=fields.split(","))
    updated = False
    if request.method == "POST":
        form = form_class(request.POST, instance=instance)
        if form.is_valid():
            print("Valid")
            form.save()
            updated = getattr(instance, fields.split(",")[0])
            # updated = getattr(instance, "name")
            return render(request, "core/update_object.html", {"updated": updated})
        else:
            print(form.errors)
    form = form_class(instance=instance)
    return render(request, "core/update_object.html", {"form": form})


type_map = {
    "project": "projects.Project",
    "dataset": "datasets.Dataset",
    "sample": "samples.Sample",
}


class DescriptionCreateView(CreateView):
    form_class = DescriptionForm
    template_name = "core/description.html"
    related_field = "descriptions"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Description Edit"
        return context

    def dispatch(self, request, *args, **kwargs):
        self.fields = self.request.GET.get("fields")
        self.fragment = self.request.GET.get("fragment", "form")
        self.success_url = self.request.GET.get("next", None)
        self.related_pk = self.kwargs.get("pk", None)
        self.related_model = self.get_related_model()
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        return {**initial, **{"object": self.related_pk}}

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(
            {
                "model": self.model,
                "request": self.request,
            }
        )
        return kwargs

    # def get_form(self, form_class=None):
    #     form = super().get_form(form_class)
    #     form.fields["type"].widget.choices = self.model.type_vocab.choices

    #     form.fields["object"].widget = form.fields["object"].hidden_widget()
    #     return form

    def get_related_model(self):
        return apps.get_model(type_map[self.kwargs["object_type"]])

    @property
    def model(self):
        # get the correct Description model based on self.related_model and the name of the related field
        model = self.related_model._meta.get_field(self.related_field).related_model

        print(model)
        return model

    def get_form_class(self):
        return modelform_factory(self.model, self.form_class, fields=self.fields)


# class DescriptionBase(LoginRequiredMixin):
#     model = Description
#     form_class = GenericDescriptionForm
#     template_name = "core/description.html"

#     def dispatch(self, request, *args, **kwargs):
#         model_class = apps.get_model(type_map[self.kwargs["object_type"]])

#         self.ctype = ContentType.objects.get_for_model(model_class)

#         self.content_object = model_class.objects.get(pk=self.kwargs["pk"])
#         return super().dispatch(request, *args, **kwargs)

#     def get_object(self, queryset=None):
#         return Description.objects.filter(
#             content_type=self.ctype,
#             object_id=self.content_object.id,
#             type=self.kwargs.get("dtype"),
#         ).first()

#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         kwargs.update({"obj": self.content_object})
#         return kwargs

#     def get_form_class(self):
#         return (
#             modelform_factory(Description, form=GenericDescriptionForm, exclude=["type"])
#             if self.object
#             else GenericDescriptionForm
#         )

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context.update(
#             {
#                 "object": self.content_object,
#                 "dtype": self.kwargs.get("dtype"),
#                 "has_edit_permission": True,
#             }
#         )
#         return context

#     def get_success_url(self):
#         kwargs = self.kwargs
#         kwargs.update({"dtype": self.object.type})
#         return reverse("description-detail", kwargs=kwargs)


# class DescriptionDetailView(DescriptionBase, DetailView):
#     pass


# class DescriptionUpdateView(DescriptionBase, UpdateView):
#     extra_context = {"update": True}


# class DescriptionCreateView(DescriptionBase, CreateView):
#     extra_context = {"create": True}


# class DescriptionDeleteView(DescriptionBase, DeleteView):
#     pass


class PortalTeamView(TemplateView):
    template_name = "core/portal_team.html"

    def get_context_data(self):
        context = super().get_context_data()

        groups = Group.objects.prefetch_related("user_set").all()

        context.update(
            {
                "groups": groups,
            },
        )

        return context


class GenericContactForm(LoginRequiredMixin, ContactFormView):
    """A view class that will send an email to all contributors with the ContactPerson role."""

    def get_object(self, queryset=None):
        model_class = apps.get_model(type_map[self.kwargs["object_type"]])
        return model_class.objects.get(pk=self.kwargs["pk"])

    @property
    def recipient_list(self):
        self.object = self.get_object()

        contacts = self.object.contributions.filter(roles__contains=["ContactPerson"])

        # get the email addresses of the contributors
        emails = []
        for c in contacts:
            if c.profile.user:
                emails.append(c.profile.user.email)
        print(emails)
        return emails


class DirectoryView(RedirectView):
    permanent = False
    prefix_map = {
        "p": "projects.Project",
        "d": "datasets.Dataset",
        "s": "samples.Sample",
        # "m": "measurements.Measurement",
        "c": "contributors.Contributor",
    }

    def get_redirect_url(self, *args, **kwargs):
        obj_id = self.kwargs.get("pk")

        model_name = self.prefix_map[obj_id[0]]

        model = apps.get_model(model_name)

        obj = model.objects.get(pk=obj_id)

        self.url = obj.get_absolute_url()
        return super().get_redirect_url(*args, **kwargs)
