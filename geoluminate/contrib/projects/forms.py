from django import forms
from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError
from django.forms import ModelForm, widgets
from django.forms.models import BaseModelForm, construct_instance
from django.utils.translation import gettext as _
from formset.collection import FormCollection
from formset.fieldset import FieldsetMixin
from formset.widgets import SelectizeMultiple, UploadedFileInput

from geoluminate.contrib.core.forms import (
    DescriptionFormCollection,
    KeyDateFormCollection,
)

from .models import Project


class ProjectForm(FieldsetMixin, ModelForm):
    # legend = _("Project")
    # help_text = _("Add a new project.")
    # template_name = "forms/fieldset.html"

    class Meta:
        model = Project
        fields = [
            "title",
            "status",
            "tags",
        ]
        widgets = {  # noqa: RUF012
            "tags": SelectizeMultiple(),
            "image": UploadedFileInput(),
            "status": widgets.RadioSelect(),
        }


class ProjectFormCollection(FormCollection):
    project = ProjectForm()
    key_dates = KeyDateFormCollection()
