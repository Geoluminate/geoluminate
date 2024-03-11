from django import forms
from django.contrib.contenttypes.models import ContentType
from django.forms.fields import IntegerField
from django.forms.models import ModelForm, ModelFormMetaclass
from django.forms.widgets import HiddenInput
from django.utils.translation import gettext as _
from django_select2.forms import Select2MultipleWidget
from formset.fieldset import FieldsetMixin
from formset.richtext.widgets import RichTextarea
from formset.widgets import DateTimeInput
from taggit.forms import TagField

from geoluminate.contrib.datasets.models import Dataset

from .models import Description, FuzzyDate

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

    def __init__(self, obj=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # if not kwargs.get("data") and content_object:
        self.obj = obj
        self.initial["content_type"] = ContentType.objects.get_for_model(obj)
        self.initial["object_id"] = obj.pk


class GenericDescriptionForm(GenericRelationForm):
    class Meta:
        model = Description
        fields = "__all__"

    def __init__(self, obj=None, *args, **kwargs):
        kwargs.update({"obj": obj})
        super().__init__(*args, **kwargs)
        if not kwargs.get("data") and self.fields.get("type"):
            self.fields["type"] = forms.ChoiceField(choices=self.get_type_choices(), required=False)

    def get_type_choices(self):
        """Gets the allowed choices for the target object. This is used to populate the type field on the form. First, get the allowed choices from TYPE_CHOICES, then filter out any choices that are already in use by the target object."""
        used = self.obj.descriptions.values_list("type", flat=True)
        return [(c, c) for c in self.obj.DESCRIPTION_TYPES if c not in used]


class GenericForm(FieldsetMixin, ModelForm):
    id = IntegerField(required=False, widget=HiddenInput)


class FuzzyDateForm(GenericRelationForm):
    class Meta:
        model = FuzzyDate
        fields = ["type", "date"]
        widgets = {"date": DateTimeInput()}


# ===================== FORM COLLECTIONS =====================


# class FuzzyDateFormCollection(FormCollection):
#     min_siblings = 0
#     legend = _("Key Dates")
#     add_label = _("Add new")
#     related_field = "dataset"


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
        self.cleaned_data = {
            **self.cleaned_data,
            "content_type": ctype,
            "object_id": object_id,
        }

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


# class DescriptionFormCollection(FormCollection):
#     min_siblings = 0
#     extra_siblings = 0
#     description = DescriptionForm()
#     legend = _("Descriptions")
#     add_label = _("Add new")
#     related_field = "generic"

#     # def model_to_dict(self, dataset):
#     #     print("model_to_dict", dataset)

#     # def model_to_dict(self, dataset):
#     #     print("model_to_dict", dataset)

#     def construct_instance(self, instance=None):
#         for valid_holders in self.valid_holders:
#             # first, handle holders which are forms
#             for name, holder in valid_holders.items():
#                 if not isinstance(holder, BaseModelForm):
#                     continue
#                 if holder.marked_for_removal:
#                     holder.instance.delete()
#                     continue

#                 # putting this here in order to save the correct content type and object id
#                 holder.cleaned_data.update(
#                     {"content_type": ContentType.objects.get_for_model(instance), "object_id": instance.id}
#                 )

#                 construct_instance(holder, holder.instance)
#                 if getattr(self, "related_field", None):
#                     setattr(holder.instance, self.related_field, instance)

#                 try:
#                     holder.save()
#                 except (IntegrityError, ValueError) as error:
#                     # some errors are caught only after attempting to save
#                     holder._update_errors(error)

#     def retrieve_instance(self, data):
#         if data := data.get("descriptions"):
#             try:
#                 return self.instance.descriptions.get(id=data.get("id") or 0)
#             except (AttributeError, Description.DoesNotExist, ValueError):
#                 return Description(
#                     type=data.get("type"),
#                     text=data.get("text"),
#                     content_object=self.instance,
#                 )


# class DatasetFormCollection(FormCollection):
#     descriptions = DescriptionFormCollection()


class ControlledTagField(TagField, forms.ChoiceField):
    widget = Select2MultipleWidget

    def clean(self, value):
        return [value]


class ControlledMultipleTagField(TagField, forms.ChoiceField):
    widget = Select2MultipleWidget

    def clean(self, value):
        print(value)
        return value


class MultiTagFormMetaclass(ModelFormMetaclass):
    def __new__(cls, class_name, bases, attrs):
        if "Meta" in attrs:
            tag_fields = list(getattr(attrs["Meta"], "tag_fields", []))
            fieldset = set(getattr(attrs["Meta"], "fields", []))
            fieldset.update(tag_fields)
            attrs["Meta"].fields = list(fieldset)
        new_class = super().__new__(cls, class_name, bases, attrs)

        # new_class._meta.tag_fields = tag_fields
        return new_class


class MultiTagFormMixin(metaclass=MultiTagFormMetaclass):
    """A mixin for forms that have a tags field. This mixin adds a method to the form that will save the tags."""

    def __init__(self, *args, **kwargs):
        opts = self._meta
        if kwargs.get("instance"):
            initial = kwargs.get("initial", {})
            for field_name in opts.tag_fields:
                # get form field instance from name
                field = self.base_fields[field_name]

                # get choices from form field
                choices = field.choices

                # get all tags from the instance
                tags = getattr(kwargs["instance"], field.tag_field_name)

                # get all tags that appear in choices
                tags = {str(tag.pk): str(tag) for tag in tags if str(tag.pk) in dict(choices)}

                # set initial value for the form field
                initial[field_name] = tags

            kwargs.setdefault("initial", initial)
        super().__init__(*args, **kwargs)

    def _clean_form(self):
        opts = self._meta
        super()._clean_form()
        cleaned_data = {f: self.cleaned_data[f] for f in opts.untangled_fields if f in self.cleaned_data}

        # loop through tag_fields and combine into a single list of values
        for field_name in opts.tag_fields:
            if field_name not in self.cleaned_data:
                continue
            if isinstance(self.base_fields[field_name], forms.ModelMultipleChoiceField):
                cleaned_data[field_name] = self.cleaned_data[field_name]
            else:
                cleaned_data[field_name] = self.cleaned_data[field_name].values()

        self.cleaned_data = cleaned_data
