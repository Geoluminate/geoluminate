from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext as _
from entangled.forms import EntangledModelForm
from formset.collection import FormCollection

# from geoluminate.core.forms import FuzzyDateFormCollection
from .models import Project


class BaseForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        self.user = None
        if self.request:
            self.user = self.request.user

        super().__init__(*args, **kwargs)


class Options(EntangledModelForm):
    cascade_license = forms.BooleanField(
        label=_("Cascade License"),
        help_text=_("Apply license to all datasets within this project."),
        required=False,
    )

    add_dataset_contributors = forms.BooleanField(
        label=_("Add Dataset Contributors"),
        help_text=_("Dataset contributors are added as project members."),
        initial=True,
    )

    add_project_leaders = forms.BooleanField(
        label=_("Add Project Leaders"),
        help_text=_("Project leaders are added to published datasets by default."),
        initial=True,
    )

    class Meta:
        model = Project
        # fields = "__all__"
        entangled_fields = {
            "options": [
                "cascade_license",
            ]
        }


class ProjectForm(BaseForm):
    title = forms.CharField(help_text=_("Give your new project a meaningful name"))
    status = forms.ChoiceField(
        choices=Project.STATUS_CHOICES.choices,
        help_text=_("What is the current status of this project?"),
    )

    class Meta:
        model = Project
        fields = [
            "title",
            "status",
        ]


class ProjectFormCollection(FormCollection):
    project = ProjectForm()
