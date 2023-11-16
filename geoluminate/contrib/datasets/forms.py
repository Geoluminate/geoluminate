# from client_side_image_cropping import ClientsideCroppingWidget

from django import forms
from django.utils.translation import gettext as _
from formset.collection import FormCollection
from formset.fieldset import FieldsetMixin
from formset.widgets import UploadedFileInput  # DateTimeInput,
from literature import forms as lit_forms
from literature.forms import CitationJSFormMixin, OnlineSearchForm
from literature.models import Literature

from geoluminate.contrib.core.forms import DescriptionFormCollection

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


class LiteratureUploadForm(FieldsetMixin, CitationJSFormMixin, forms.ModelForm):
    """A form that renders a search bar for DOI, PMCID, PMID, Wikidata and previews the formatted content below."""

    # legend = _("Source")
    # help_text = _("Find an existing publication online using a DOI, PMCID, PMID, Wikidata QID or GitHub repository URL")
    # show_condition = "literature.form_chooser.source == 'online'"

    source = forms.ChoiceField(
        # label=_("Search for an existing DOI."),
        choices=(
            ("online", _("Review a published item with an existing DOI")),
            ("upload", _("Upload a reference from a local file")),
            ("manual", _("Manually enter details of a new reference.")),
        ),
        initial="online",
        required=False,
    )

    identifier = forms.CharField(
        label=_("Search"),
        help_text=_("Find a publication to review by entering a valid DOI"),
        widget=forms.TextInput(
            attrs={
                "onchange": "fetchCitation(event);",
                "df-show": ".source == 'online'",
            }
        ),
        required=False,
    )

    file = forms.FileField(
        label=_("Bibliography File"),
        help_text=_("Upload a bibliography file."),
        widget=UploadedFileInput(attrs={"onchange": "readFileContents(event);", "df-show": ".source == 'upload'"}),
        required=False,
    )

    pdf = forms.FileField(
        label=_("PDF File"),
        help_text=_(
            "We ask that you provide a PDF of the publication being reviewed. This file is archived to ensure"
            " persistence of all relevant documents related to data within the database. It will not be made publicly"
            " available."
        ),
        widget=UploadedFileInput(attrs={"df-hide": ".CSL == 'null'"}),
        required=False,
    )

    class Meta:
        model = Literature
        fields = [
            "source",
            "identifier",
            "file",
            "CSL",
            "preview",
            "pdf",
        ]

    def clean_identifier(self):
        """Check if this identifier is associated with a review."""
        data = self.cleaned_data["identifier"]
        # try:
        #     review_obj = Review.objects.get(dataset__reference__identifiers__ID=data)
        # except Review.DoesNotExist:
        #     pass
        # else:
        #     raise forms.ValidationError(
        #         _(f"This literature item is already under review by {review_obj.reviewer} and cannot be selected.")
        #     )
        return data


class DatasetForm(FieldsetMixin, forms.ModelForm):
    is_public = forms.ChoiceField(
        label=_("Visibility"),
        help_text=_("Choose whether this dataset is publicly discoverable."),
        choices=(
            (True, _("Public")),
            (False, _("Private")),
        ),
        initial=False,
    )

    class Meta:
        model = Dataset
        fields = [
            "is_public",
            "title",
        ]
        # fields = ["project", "title"]


class DatasetFormCollection(FormCollection):
    descriptions = DescriptionFormCollection()


class LiteratureFormCollection(FormCollection):
    literature = lit_forms.LiteratureForm()
