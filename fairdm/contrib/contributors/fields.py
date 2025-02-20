from django import forms


class OrcidInputWidget(forms.TextInput):
    template_name = "widgets/orcid_input.html"
