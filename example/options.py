from fairdm.metadata import Metadata

from .models import CustomSample


class CustomSampleMeta(Metadata):
    model = CustomSample
