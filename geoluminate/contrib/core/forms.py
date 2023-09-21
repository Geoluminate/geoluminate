# from client_side_image_cropping import ClientsideCroppingWidget
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.forms import widgets
from django.forms.fields import IntegerField
from django.forms.models import ModelForm, construct_instance, model_to_dict
from django.forms.widgets import HiddenInput
from django.utils.translation import gettext as _
from formset.collection import FormCollection
from formset.fieldset import Fieldset, FieldsetMixin
from formset.renderers import bootstrap
from formset.richtext.widgets import RichTextarea
from formset.utils import FormMixin
from formset.widgets import (  # DateTimeInput,
    DateInput,
    DualSortableSelector,
    Selectize,
    SelectizeMultiple,
    UploadedFileInput,
)

from geoluminate.contrib.contributor.forms import ProfileFormNoImage
from geoluminate.contrib.contributor.models import Contribution, Contributor
from geoluminate.utils.forms import DefaultFormRenderer

from .models import Dataset, Description, KeyDate, Project

# ===================== FORMS =====================

TYPE_CHOICES = {
    "core.Dataset": [
        ("Abstract", _("Abstract")),
        ("Methods", _("Methods")),
    ],
}


class GenericDescriptionForm(forms.ModelForm):
    # will probably need a check in this form somewhere to make sure
    # the user adding/editing the description is allowed to do so
    content_type = forms.ModelChoiceField(
        queryset=ContentType.objects.all(),
        widget=forms.HiddenInput,
    )
    object_id = forms.IntegerField(widget=forms.HiddenInput)

    class Meta:
        model = Description
        fields = "__all__"

    def __init__(self, obj, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.initial["content_type"] = ContentType.objects.get_for_model(obj)
        self.initial["object_id"] = obj.pk
        lookup = f"{obj._meta.app_label}.{obj._meta.model_name.title()}"
        self.fields["type"].choices = TYPE_CHOICES.get(lookup)


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
            # "tags": SelectizeMultiple(choices=Project.PROJECT_TAGS.choices),
            "tags": SelectizeMultiple(),
            # "image": ImageWidget(
            #     width=1200,
            #     height=630,
            #     preview_width=300,
            #     preview_height=157,
            #     format="webp",
            # ),
            "image": UploadedFileInput(),
            # "image": ImageWidget(),
            "status": widgets.RadioSelect(),
        }


class GenericForm(FieldsetMixin, ModelForm):
    id = IntegerField(required=False, widget=HiddenInput)

    # @property
    # def legend(self):
    #     return self.instance._meta.verbose_name.title()


class DatasetForm(FieldsetMixin, ModelForm):
    class Meta:
        model = Dataset
        fields = ["title"]


class KeyDateForm(GenericForm):
    class Meta:
        model = KeyDate
        fields = ["id", "type", "date"]
        # widgets = {"date": DateTimeInput()}


# class DatasetForm(GenericForm):
#     class Meta:
#         model = Dataset
#         fields = ["title"]


class DescriptionForm(GenericForm):
    class Meta:
        model = Description
        fields = ["id", "type", "text"]
        widgets = {"description": RichTextarea()}


class ContributionForm(GenericForm):
    profile = forms.ModelChoiceField(
        queryset=Contributor.objects.all(),
        widget=Selectize(
            search_lookup="name__icontains",
            placeholder="Select contributor",
        ),
    )

    class Meta:
        model = Contribution
        fields = [
            "id",
            "profile",
            "roles",
        ]
        widgets = {"roles": SelectizeMultiple(choices=Contribution.CONTRIBUTOR_ROLES.choices)}


# ===================== FORM COLLECTIONS =====================


class KeyDateFormCollection(FormCollection):
    min_siblings = 0
    key_date = KeyDateForm(renderer=DefaultFormRenderer(field_css_classes={"*": "col", "type": "col-4"}))
    legend = _("Key Dates")
    add_label = _("Add new")
    related_field = "project"

    def retrieve_instance(self, data):
        if data := data.get("key_date"):
            try:
                return self.instance.key_dates.get(id=data.get("id") or 0)
            except (AttributeError, Dataset.DoesNotExist, ValueError):
                return KeyDate(date=data.get("date"), project=self.instance)


class DescriptionFormCollection(FormCollection):
    min_siblings = 0
    extra_siblings = 0
    descriptions = DescriptionForm()
    legend = _("Descriptions")
    add_label = _("Add new")
    related_field = "project"

    help_text = _(
        "Create descriptions for your project using the available description types. These descriptions greatly enhance"
        " the discoverability of your project and can help you reach a wider audience."
    )

    def retrieve_instance(self, data):
        if data := data.get("dataset"):
            try:
                return self.instance.descriptions.get(id=data.get("id") or 0)
            except (AttributeError, Description.DoesNotExist, ValueError):
                return Description(title=data.get("type"), project=self.instance)


class DatasetFormCollection(FormCollection):
    min_siblings = 0
    extra_siblings = 0
    dataset = DatasetForm()
    # descriptions = DescriptionFormCollection(min_siblings=1, extra_siblings=1)

    legend = _("Datasets")
    add_label = _("Add new")
    related_field = "project"

    help_text = _("Add datasets to your project.")

    def retrieve_instance(self, data):
        if data := data.get("dataset"):
            try:
                return self.instance.datasets.get(id=data.get("id") or 0)
            except (AttributeError, Dataset.DoesNotExist, ValueError):
                return Dataset(title=data.get("title"), project=self.instance)


class ContributionFormCollection(FormCollection):
    min_siblings = 0
    extra_siblings = 0
    contributors = ContributionForm()
    # descriptions = DescriptionFormCollection(min_siblings=1, extra_siblings=1)

    legend = _("Contributions")
    add_label = _("Add new")
    related_field = "contributors"

    help_text = _("Add contributors to your project.")

    def retrieve_instance(self, data):
        if data := data.get("contributors"):
            try:
                return self.instance.contributors.get(id=data.get("id") or 0)
            except (AttributeError, Contribution.DoesNotExist, ValueError):
                return Contribution(title=data.get("title"), project=self.instance)


class ProjectFormCollection(FormCollection):
    project = ProjectForm()
    descriptions = DescriptionFormCollection()
    contributors = ContributionFormCollection()
    key_dates = KeyDateFormCollection()
    datasets = DatasetFormCollection()


class DatasetFormCollection(FormCollection):
    dataset = DatasetForm()
    descriptions = DescriptionFormCollection()
    contributors = ContributionFormCollection()
    key_dates = KeyDateFormCollection()
