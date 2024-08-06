from crispy_forms.layout import Layout

from geoluminate.contrib.core.filters import BaseListFilter

from .models import Dataset


class DatasetFilter(BaseListFilter):
    class Meta:
        model = Dataset
        exclude = ["options", "image"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sidebar.layout = Layout(
            "license",
        )
