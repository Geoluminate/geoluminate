from crispy_forms.helper import FormHelper
from django import forms

from ..models import Organization


class RORWidget(forms.TextInput):
    template_name = "widgets/ror.html"


class RORForm(forms.ModelForm):
    data = forms.JSONField(label=False, required=True, widget=RORWidget())

    class Meta:
        model = Organization
        fields = ["data"]

    def __init__(self, *args, **kwargs):
        if "request" in kwargs:
            self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "RORForm"
        # self.helper.form_action = reverse("organizations:organization-create")
