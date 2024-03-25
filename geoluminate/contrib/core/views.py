from actstream import actions
from django.apps import apps
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.forms import modelform_factory
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django_contact_form.views import ContactFormView

from .forms import GenericDescriptionForm
from .models import Description


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


@login_required
def manage_description(request, object_type, uuid, dtype=None):
    """Returns a form for managing the description of the given object.

    If dtype matches a description related to the object, the form will be populated with the existing description.

    If dtype is empty, a form will be initialised with a new description related to the object.

    """

    type_map = {
        "p": "geoluminate.Project",
        "d": "geoluminate.Dataset",
        "s": "geoluminate.Sample",
    }

    ctype = ContentType.objects.get_for_model(apps.get_model(type_map[object_type]))

    # the object being described
    obj = get_object_or_404(ctype.model_class(), uuid=uuid)

    # the description object
    description = obj.descriptions.get(type=dtype)

    # the description form
    form_class = (
        modelform_factory(Description, form=GenericDescriptionForm, exclude=["type"])
        if description
        else GenericDescriptionForm
    )

    context = {
        "description": description,
        "object": obj,
        "dtype": dtype,
        "has_edit_permission": True,
    }

    if request.method == "POST":
        form = form_class(data=request.POST, instance=description, obj=obj)
        if form.is_valid():
            form.save()
            context.update({"form": form, "editing": False})
            return render(request, "core/description.html", context)
        else:
            print(form.errors)

    form = form_class(instance=description, obj=obj)

    context.update({"form": form, "editing": True})

    return render(request, "core/description.html", context)


type_map = {
    "p": "geoluminate.Project",
    "d": "geoluminate.Dataset",
    "s": "geoluminate.Sample",
}


class GenericBaseView:
    """A base class for generic views that can be applied to any Geoluminate object type that has a uuid(Project, Dataset, Sample). The url for such a view should include the object type and the uuid in the form "<obj_type>/<uuid>/". (e.g. /p/uuid/ or /d/uuid/ or /s/uuid/)"""

    slug_field = "uuid"
    slug_url_kwarg = "uuid"

    def get_object(self, queryset=None):
        model_class = apps.get_model(type_map[self.kwargs["object_type"]])
        return model_class.objects.get(uuid=self.kwargs["uuid"])


class DescriptionBase(LoginRequiredMixin):
    model = Description
    slug_field = "uuid"
    slug_url_kwarg = "uuid"
    form_class = GenericDescriptionForm
    template_name = "core/description.html"

    def dispatch(self, request, *args, **kwargs):
        model_class = apps.get_model(type_map[self.kwargs["object_type"]])

        self.ctype = ContentType.objects.get_for_model(model_class)

        self.content_object = model_class.objects.get(uuid=self.kwargs["uuid"])
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return Description.objects.filter(
            content_type=self.ctype,
            object_id=self.content_object.id,
            type=self.kwargs.get("dtype"),
        ).first()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"obj": self.content_object})
        return kwargs

    def get_form_class(self):
        return (
            modelform_factory(Description, form=GenericDescriptionForm, exclude=["type"])
            if self.object
            else GenericDescriptionForm
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "object": self.content_object,
                "dtype": self.kwargs.get("dtype"),
                "has_edit_permission": True,
            }
        )
        return context

    def get_success_url(self):
        kwargs = self.kwargs
        kwargs.update({"dtype": self.object.type})
        return reverse("description-detail", kwargs=kwargs)


class DescriptionDetailView(DescriptionBase, DetailView):
    pass


class DescriptionUpdateView(DescriptionBase, UpdateView):
    extra_context = {"update": True}


class DescriptionCreateView(DescriptionBase, CreateView):
    extra_context = {"create": True}


class DescriptionDeleteView(DescriptionBase, DeleteView):
    pass


class GenericContactForm(LoginRequiredMixin, ContactFormView):
    """A view class that will send an email to all contributors with the ContactPerson role. The url for such a view should include the object type and the uuid in the form "<obj_type>/<uuid>/". (e.g. /p/uuid/ or /d/uuid/ or /s/uuid/)"""

    def get_object(self, queryset=None):
        model_class = apps.get_model(type_map[self.kwargs["object_type"]])
        return model_class.objects.get(uuid=self.kwargs["uuid"])

    @property
    def recipient_list(self):
        self.object = self.get_object()

        contacts = self.object.contributors.filter(roles__contains=["ContactPerson"])

        # get the email addresses of the contributors
        emails = []
        for c in contacts:
            if c.profile.user:
                emails.append(c.profile.user.email)
        print(emails)
        return emails
