from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext as _
from polymorphic_treebeard.forms import movepolynodeform_factory

from geoluminate.forms import ImageCroppingWidget

from .models import Dataset, Project, Sample


class BaseForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        self.user = None
        if self.request:
            self.user = self.request.user

        super().__init__(*args, **kwargs)


class ProjectForm(BaseForm):
    image = forms.ImageField(
        widget=ImageCroppingWidget(
            width=1200,
            height=int(1200 * 9 / 16),
            empty_text=_("Select cover image"),
            config={
                "enableOrientation": True,
            },
            result={
                "format": "jpeg",
            },
        ),
        required=False,
        label=False,
    )
    name = forms.CharField(label=_("Project name"), help_text=_("Give your new project a name"))
    status = forms.ChoiceField(
        label=_("Current status"),
        choices=Project.STATUS_CHOICES.choices,
        help_text=_("In which stage of it's lifecycle is this project?"),
    )

    class Meta:
        model = Project
        fields = [
            "image",
            "name",
            "status",
        ]


class DatasetForm(BaseForm):
    """Generic form used by DataestCRUDView for creating and updating regular fields on a Dataset."""

    image = forms.ImageField(
        widget=ImageCroppingWidget(
            width=1200,
            height=int(1200 * 9 / 16),
            config={
                "enableOrientation": True,
            },
            result={
                "format": "jpeg",
            },
        ),
        required=False,
        label=False,
    )

    class Meta:
        model = Dataset
        fields = ["image", "project", "name", "license", "visibility"]

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        if self.request:
            self.fields["project"].queryset = self.request.user.projects.all()
        # self.fields["project"].widget = forms.HiddenInput()
        # self.fields["visibility"].initial = Dataset.VISIBILITY_PRIVATE


SampleFormMixin = movepolynodeform_factory(
    Sample, exclude=["created", "modified", "keywords", "options", "path", "numchild"]
)


class SampleForm(SampleFormMixin):
    _position = forms.ChoiceField(required=True, label=_("Position"), widget=forms.HiddenInput)
    _ref_node_id = forms.ChoiceField(
        label=_("Child of"),
        help_text=_("The sample from which this sample was derived, if any."),
        required=False,
    )

    class Meta:
        model = Sample

        exclude = ["created", "modified", "keywords", "depth", "options", "path", "numchild"]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)
        if self.request:
            self.fields["dataset"].queryset = self.request.user.datasets.all()
        self.fields["dataset"].initial = self.request.GET.get("dataset")

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance
