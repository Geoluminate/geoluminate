from django import forms

from .models import Sample


class SampleForm(forms.ModelForm):
    class Meta:
        model = Sample
        # fields = ["dataset", "name"]
        exclude = ["created", "modified", "keywords", "options", "path", "depth", "numchild"]
