from .models import Sample


def get_portal_samples():
    return Sample.objects.all().order_by("title")
