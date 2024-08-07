from django import forms

from .models import BaseSample, Location


class SampleForm(forms.ModelForm):
    class Meta:
        model = BaseSample
        # fields = ["dataset", "name"]
        exclude = ["created", "modified", "keywords"]


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ["point"]
