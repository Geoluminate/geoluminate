from django.utils.translation import gettext as _
from literature.models import LiteratureItem

from geoluminate.views import BaseListView


class ReferenceListView(BaseListView):
    title = _("References")
    model = LiteratureItem
    template_name = "geoluminate/base/list_view.html"
    queryset = LiteratureItem.objects.all()
    filterset_fields = [
        "title",
    ]
