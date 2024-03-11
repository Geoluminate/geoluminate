# from client_side_image_cropping import ClientsideCroppingWidget

from django import forms
from django.utils.translation import gettext as _
from formset.collection import FormCollection
from formset.fieldset import FieldsetMixin

# from geoluminate.contrib.core.forms import DescriptionFormCollection
from .models import Dataset


class ImportOptions(FieldsetMixin, forms.Form):
    legend = _("Options")
    help_text = _("Customise how the review process should be started.")

    parse_authors = forms.BooleanField(
        label=_("Parse authors?"),
        help_text=_(
            "Do you want to automatically parse author names and add them as dataset contributors? You can always add"
            " more or modify contributors later."
        ),
        initial=True,
    )


class DatasetForm(FieldsetMixin, forms.ModelForm):
    class Meta:
        model = Dataset
        fields = ["visibility", "title"]


class DatasetFormCollection(FormCollection):
    pass
    # descriptions = DescriptionFormCollection()
