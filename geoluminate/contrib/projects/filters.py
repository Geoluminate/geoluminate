from crispy_forms.layout import Layout

from geoluminate.contrib.core.filters import BaseListFilter

from .models import Project


class ProjectFilter(BaseListFilter):
    class Meta:
        model = Project
        exclude = ["options", "image", "funding"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sidebar.layout = Layout(
            "status",
        )
