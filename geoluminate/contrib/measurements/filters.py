from geoluminate.core.filters import BaseListFilter

from .models import Measurement


class MeasurementFilter(BaseListFilter):
    class Meta:
        model = Measurement
        exclude = ["options", "image"]

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # self.layout = Layout(
    #     #     # "license",
    #     # )
