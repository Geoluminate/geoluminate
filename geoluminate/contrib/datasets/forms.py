from django import forms

from geoluminate.contrib.projects.forms import BaseForm
from geoluminate.forms import ImageCroppingWidget

from .models import Dataset


class DatasetForm(BaseForm):
    """Generic form used by DataestCRUDView for creating and updating regular fields on a Dataset."""

    image = forms.ImageField(
        widget=ImageCroppingWidget(
            width=1200,
            height=int(1200 * 9 / 16),
            config={
                "enableOrientation": True,
            },
            result={
                "format": "jpeg",
            },
        ),
        required=False,
        label=False,
    )

    class Meta:
        model = Dataset
        fields = ["image", "project", "title", "license", "visibility"]

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        if self.request:
            self.fields["project"].queryset = self.request.user.projects.all()
        # self.fields["project"].widget = forms.HiddenInput()
        # self.fields["visibility"].initial = Dataset.VISIBILITY_PRIVATE


# class MoveDatasetForm(BaseForm):
#     """Form used used to update the project that a Dataset belongs to."""

#     class Meta:
#         model = Dataset
#         fields = "__all__"

#     def __init__(self, request=None, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.request = request
#         if self.request:
#             self.fields["project"].queryset = self.request.user.projects.all()
