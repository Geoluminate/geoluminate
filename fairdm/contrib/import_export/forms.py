from django import forms

from .utils import export_choices, import_choices


class ImportForm(forms.Form):
    file = forms.FileField(
        help_text=f"Select a file to import. The following formats are supported: {', '.join(import_choices)}."
    )


class ExportForm(forms.Form):
    format = forms.ChoiceField(choices=export_choices)
