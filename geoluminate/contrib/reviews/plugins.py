from django.core.files.base import ContentFile
from django.utils.text import slugify
from django.utils.translation import gettext as _
from django.views.generic import DetailView, TemplateView, UpdateView
from django_downloadview.views import VirtualDownloadView
from formset.views import FileUploadMixin, FormViewMixin

from geoluminate.plugins import review
from geoluminate.utils import icon

# from .filters import DatasetFilter
# from .forms import DatasetForm
from .models import Review
from .views import ReviewDetailView


@review.page("overview", icon="fas fa-book-open")
class DatasetOverview(ReviewDetailView, FileUploadMixin, FormViewMixin, UpdateView):
    model = Review
    template_name = "geoluminate/plugins/overview.html"
    slug_field = "pk"
    slug_url_kwarg = "pk"

    def has_edit_permission(self):
        """TODO: Add permissions."""
        # return self.request.user.is_superuser
        return None
