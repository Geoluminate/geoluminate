from django.forms import fields, forms
from django.forms.models import ModelForm, construct_instance, model_to_dict
from django.utils.translation import gettext as _
from formset.collection import FormCollection
from formset.fieldset import FieldsetMixin
from formset.renderers import bootstrap
from formset.richtext.widgets import RichTextarea
from formset.utils import FormMixin
from formset.widgets import DateInput, DualSortableSelector, UploadedFileInput

from .models import Dataset, Project


class ProjectForm(ModelForm):
    default_renderer = bootstrap.FormRenderer()

    class Meta:
        model = Project
        fields = [  # noqa: RUF012
            "status",
            "start_date",
            "end_date",
            "name",
            "description",
        ]
        widgets = {  # noqa: RUF012
            "description": RichTextarea(attrs={"min-height": "300px"}),
            "start": DateInput(attrs={"show-if": ".status!=0"}),
            "end": DateInput(attrs={"show-if": ".status!=0"}),
            # "authors": DualSortableSelector,  # or DualSelector
        }


# class DatasetFileForm(ModelForm):
#     class Meta:
#         model = Dataset
#         fields = ["file"]
#         widgets = {
#             "file": UploadedFileInput(),
#         }


# class DatasetFileCollection(FormCollection):
#     legend = "Supplementary Material"
#     min_siblings = 0
#     extra_siblings = 1
#     default_renderer = bootstrap.FormRenderer()

#     supplementary_material = DatasetFileForm()

# def model_to_dict(self, literature):
#     opts = self.declared_holders["supps"]._meta
#     return [{"supp": model_to_dict(supp, fields=opts.fields)} for supp in literature.supplementary.all()]

# def construct_instance(self, literature, data):
#     for d in data:
#         try:
#             supp_object = literature.supplementary.get(id=d["supplementary"]["id"])
#         except (KeyError, Dataset.DoesNotExist):
#             supp_object = Dataset(literature=literature)
#         form_class = self.declared_holders["supps"].__class__
#         form = form_class(data=d["supplementary"], instance=supp_object)
#         if form.is_valid():
#             if form.marked_for_removal:
#                 supp_object.delete()
#             else:
#                 construct_instance(form, supp_object)
#                 form.save()
