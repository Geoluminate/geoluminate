from geoluminate.core.filters import BaseListFilter

from .models import Dataset


class DatasetFilter(BaseListFilter):
    class Meta:
        model = Dataset
        exclude = ["options", "image"]
