from geoluminate.core.filters import BaseListFilter

from .models import Project


class ProjectFilter(BaseListFilter):
    class Meta:
        model = Project
        exclude = ["options", "image", "funding"]
