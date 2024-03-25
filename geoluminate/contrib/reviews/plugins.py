from django.views.generic import UpdateView
from formset.views import FileUploadMixin, FormViewMixin

from geoluminate.contrib.contributors.utils import current_user_has_role
from geoluminate.plugins import PluginRegistry
from geoluminate.utils import icon

from .forms import ReviewForm
from .models import Review
from .views import ReviewDetailView

review = PluginRegistry("reviews", base=ReviewDetailView)


@review.page("overview", icon=icon("overview"))
class ReviewOverview(ReviewDetailView, FileUploadMixin, FormViewMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = "geoluminate/plugins/overview.html"

    def has_edit_permission(self):
        """TODO: Add permissions."""
        return current_user_has_role(self.request, self.object, "Creator")
