from django import forms

from .models import Location, Sample


class SampleForm(forms.ModelForm):
    class Meta:
        model = Sample
        # fields = ["dataset", "name"]
        exclude = ["created", "modified", "keywords"]


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ["point"]
