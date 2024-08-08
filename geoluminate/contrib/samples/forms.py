from django import forms

from .models import BaseSample


class SampleForm(forms.ModelForm):
    class Meta:
        model = BaseSample
        # fields = ["dataset", "name"]
        exclude = ["created", "modified", "keywords"]
