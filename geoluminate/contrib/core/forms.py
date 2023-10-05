# from client_side_image_cropping import ClientsideCroppingWidget
from typing import Any

from django import forms
from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError
from django.forms.fields import IntegerField
from django.forms.models import (
    BaseModelForm,
    ModelForm,
    construct_instance,
    model_to_dict,
)
from django.forms.widgets import HiddenInput
from django.utils.translation import gettext as _
from formset.collection import FormCollection
from formset.fieldset import FieldsetMixin
from formset.richtext.widgets import RichTextarea
from formset.widgets import (  # DateTimeInput,
    DateInput,
    DateTimeInput,
    DualSortableSelector,
    Selectize,
    SelectizeMultiple,
    UploadedFileInput,
)

from geoluminate.contrib.contributors.forms import ProfileFormNoImage
from geoluminate.contrib.contributors.models import Contribution, Contributor
from geoluminate.utils.forms import DefaultFormRenderer

from .models import Description, KeyDate

# ===================== FORMS =====================

TYPE_CHOICES = {
    "core.Dataset": [
        ("Abstract", _("Abstract")),
        ("Methods", _("Methods")),
    ],
}


class GenericRelationForm(forms.ModelForm):
    # will probably need a check in this form somewhere to make sure
    # the user adding/editing the description is allowed to do so
    content_type = forms.ModelChoiceField(
        required=False,
        queryset=ContentType.objects.all(),
        widget=forms.HiddenInput,
    )
    object_id = forms.IntegerField(required=False, widget=forms.HiddenInput)

    def __init__(self, content_object=None, *args, **kwargs):
        print(kwargs)
        super().__init__(*args, **kwargs)
        # if not kwargs.get("data") and content_object:
        # self.content_object = content_object
        # self.initial["content_type"] = ContentType.objects.get_for_model(content_object)
        # self.initial["object_id"] = content_object.pk


class GenericDescriptionForm(GenericRelationForm):
    class Meta:
        model = Description
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not kwargs.get("data"):
            self.fields["type"].choices = self.get_type_choices()

    def get_type_choices(self):
        """Gets the allowed choices for the target object. This is used to populate the type field on the form. First, get the allowed choices from TYPE_CHOICES, then filter out any choices that are already in use by the target object."""
        used_choices = self.content_object.descriptions.values_list("type", flat=True)
        return [choice for choice in self.content_object.DESCRIPTION_TYPES if choice[0] not in used_choices]


# class ProjectForm(FieldsetMixin, ModelForm):
#     # legend = _("Project")
#     # help_text = _("Add a new project.")
#     # template_name = "forms/fieldset.html"

#     class Meta:
#         model = Project
#         fields = [
#             "title",
#             "status",
#             "tags",
#         ]
#         widgets = {  # noqa: RUF012
#             "tags": SelectizeMultiple(),
#             "image": UploadedFileInput(),
#             "status": widgets.RadioSelect(),
#         }


class GenericForm(FieldsetMixin, ModelForm):
    id = IntegerField(required=False, widget=HiddenInput)

    # @property
    # def legend(self):
    #     return self.instance._meta.verbose_name.title()


# class DatasetForm(FieldsetMixin, ModelForm):
#     class Meta:
#         model = Dataset
#         fields = ["title"]


class KeyDateForm(GenericRelationForm):
    class Meta:
        model = KeyDate
        fields = ["type", "date"]
        widgets = {"date": DateTimeInput()}


# class ContributionForm(GenericForm):
#     profile = forms.ModelChoiceField(
#         queryset=Contributor.objects.all(),
#         widget=Selectize(
#             search_lookup="name__icontains",
#             placeholder="Select contributor",
#         ),
#     )

#     class Meta:
#         model = Contribution
#         fields = [
#             "id",
#             "profile",
#             "roles",
#         ]
#         widgets = {"roles": SelectizeMultiple(choices=Contribution.CONTRIBUTOR_ROLES.choices)}


# ===================== FORM COLLECTIONS =====================


class KeyDateFormCollection(FormCollection):
    min_siblings = 0
    key_date = KeyDateForm(renderer=DefaultFormRenderer(field_css_classes={"*": "col", "type": "col-4"}))
    legend = _("Key Dates")
    add_label = _("Add new")
    related_field = "dataset"


# class DatasetFormCollection(FormCollection):
#     min_siblings = 0
#     extra_siblings = 0
#     dataset = DatasetForm()
#     # key_dates = KeyDateFormCollection()
#     # key_dates.related_field = "dataset"

#     legend = _("Datasets")
#     add_label = _("Add new")
#     related_field = "project"

#     help_text = _("Add datasets to your project.")

#     # def retrieve_instance(self, data):
#     #     if data := data.get("dataset"):
#     #         # instance, created = Dataset.objects.get_or_create(id=data.get("id"), defaults={**data, "project":self.instance})
#     #         try:
#     #             return self.instance.datasets.get(id=data.get("id") or 0)
#     #         except (AttributeError, Dataset.DoesNotExist, ValueError):
#     #             return Dataset(title=data.get("title"), project=self.instance)


# class ContributionFormCollection(FormCollection):
#     min_siblings = 0
#     extra_siblings = 0
#     contributors = ContributionForm()
#     # descriptions = DescriptionFormCollection(min_siblings=1, extra_siblings=1)

#     legend = _("Contributions")
#     add_label = _("Add new")
#     related_field = "contributors"

#     help_text = _("Add contributors to your project.")

#     def retrieve_instance(self, data):
#         if data := data.get("contributors"):
#             try:
#                 return self.instance.contributors.get(id=data.get("id") or 0)
#             except (AttributeError, Contribution.DoesNotExist, ValueError):
#                 return Contribution(title=data.get("title"), project=self.instance)


# class ProjectFormCollection(FormCollection):
#     project = ProjectForm()
#     key_dates = KeyDateFormCollection()
#     # descriptions = DescriptionFormCollection()
#     # contributors = ContributionFormCollection()
#     # datasets = DatasetFormCollection()


class DescriptionForm(GenericRelationForm):
    min_siblings = 0
    extra_siblings = 0

    class Meta:
        model = Description
        fields = ["id", "content_type", "object_id", "type", "text"]
        widgets = {"description": RichTextarea()}

    def full_clean(self):
        return super().full_clean()

    def save(self, commit=True):
        return super().save(commit)

    def construct_instance(self, instance, cleaned_data=None):
        # content_type = ctype
        # Description.objects.first()
        # self.cleaned_data.update({"content_type": content_type, "object_id": object_id})
        # instance.content_type = content_type
        # instance.object_id = object_id
        # return instance
        # self.cleaned
        # data = self.cleaned_data
        ctype = ContentType.objects.get_for_model(Dataset)
        object_id = instance.generic.id

        # Create a copy of self.cleaned_data with the updates
        self.cleaned_data = {**self.cleaned_data, "content_type": ctype, "object_id": object_id}

        # pprint.pprint(self.cleaned_data)
        # obj = construct_instance(self, instance)
        # print(obj)
        # return obj
        # form = DescriptionForm(data=data)
        # form.is_valid()

    # def construct_instance(self, dataset):
    # print("construct_instance", dataset)
    # def construct_instance(self, instance):
    #     print("construct_instance", type(instance))
    #     # try:
    #     #     description = dataset.descriptions.get(id=self.cleaned_data.get("id") or 0)
    #     # except Description.DoesNotExist:
    #     #     description = Description(content_object=dataset)

    #     # print(self.data)
    #     # print(model_to_dict(instance))
    #     form = DescriptionForm(data=self.cleaned_data, content_object=instance)
    #     # if form.is_valid():
    #     #     # x = construct_instance(form, instance)
    #     #     # print(x)
    #     #     form.save()


class DescriptionFormCollection(FormCollection):
    min_siblings = 0
    extra_siblings = 0
    description = DescriptionForm()
    legend = _("Descriptions")
    add_label = _("Add new")
    related_field = "generic"

    # def model_to_dict(self, dataset):
    #     print("model_to_dict", dataset)

    # def model_to_dict(self, dataset):
    #     print("model_to_dict", dataset)

    def construct_instance(self, instance=None):
        for valid_holders in self.valid_holders:
            # first, handle holders which are forms
            for name, holder in valid_holders.items():
                if not isinstance(holder, BaseModelForm):
                    continue
                if holder.marked_for_removal:
                    holder.instance.delete()
                    continue

                # putting this here in order to save the correct content type and object id
                holder.cleaned_data.update(
                    {"content_type": ContentType.objects.get_for_model(instance), "object_id": instance.id}
                )

                construct_instance(holder, holder.instance)
                if getattr(self, "related_field", None):
                    setattr(holder.instance, self.related_field, instance)

                try:
                    holder.save()
                except (IntegrityError, ValueError) as error:
                    # some errors are caught only after attempting to save
                    holder._update_errors(error)

    def retrieve_instance(self, data):
        if data := data.get("descriptions"):
            try:
                return self.instance.descriptions.get(id=data.get("id") or 0)
            except (AttributeError, Description.DoesNotExist, ValueError):
                return Description(
                    type=data.get("type"),
                    text=data.get("text"),
                    content_object=self.instance,
                )


# class DatasetFormCollection(FormCollection):
#     descriptions = DescriptionFormCollection()
