from typing import Any

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from literature.formset import LiteratureFileCollection
from literature.models import Literature
from literature.views import LiteratureDetail, LiteratureEditView, LiteratureViewMixin

from geoluminate.contrib.datasets.filters import ReviewFilter
from geoluminate.db.models import Dataset
from geoluminate.views import BaseCreateView, BaseDetailView, BaseListView, HTMXMixin

from .forms import LiteratureFormCollection, LiteratureUploadForm  # LiteratureForm,
from .models import Review


class ReviewCreateView(BaseCreateView):
    model = Literature
    form_class = LiteratureUploadForm
    title = _("Start a new review")
    help_text = _(
        f"You're about to start a new review for the {settings.GEOLUMINATE['database']['name']}. Reviews are a way for"
        " community members to contribute existing data to the repository without claiming ownership of that data."
        " Make sure you have the right to contribute the data you are about to add. If you are the owner of the data,"
        " consider adding it as a dataset instead."
    )

    def form_valid(self, form):
        # THE ORDER HERE NEEDS TO BE WORKED OUT
        self.dataset = Dataset()
        response = super().form_valid(form)
        self.dataset.title = self.object.title
        self.dataset.reference = self.object
        self.dataset.save()
        self.review = self.create_review()
        return response

    def create_dataset(self):
        dataset = Dataset.objects.create(
            title=self.object.title,
            reference=self.object,
        )
        dataset.save()
        return dataset

    def create_review(self):
        review = Review.objects.create(
            dataset=self.dataset,
            reviewer=self.request.user,
        )
        review.save()
        return review

    def get_success_url(self):
        return self.dataset.get_edit_url()


class ReviewListView(BaseListView):
    """A view that lists a set of Review objects."""

    template_name = "reviews/review_list.html"

    filterset_class = ReviewFilter
    queryset = Dataset.objects.filter().order_by("-created")


class ReviewDetailView(BaseDetailView):
    model = Review
    # navigation = settings.GEOLUMINATE_PROJECT_PAGES


class ReviewDataUploadView(ReviewDetailView):
    """A view to handle uploading and verification of submitted data."""

    template_name = "datasets/literature_form.html"


class ReviewLiteratureEdit(HTMXMixin, LiteratureEditView):
    collection_class = LiteratureFormCollection
    template_name = "literature/literature_form.html"
    title = _("Confirm literature details")
    help_text = _(
        "Please confirm that the details of the chosen literature item are correct to the best of your knowledge"
    )

    def get_object(self):
        return self.get_queryset().get(dataset__review__uuid=self.kwargs.get("uuid"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["navigation"] = self.navigation
        context["title"] = self.title
        context["help_text"] = self.help_text
        context["review_object"] = self.object.dataset.review
        return context


class ReviewFilesEdit(ReviewLiteratureEdit):
    collection_class = LiteratureFileCollection
    title = _("File Upload")
    help_text = _(
        "Please upload here any files used during the revision of this dataset. Files are stored for archival purposes"
        " only and are not shared publicly. "
    )


class LiteratureReviewListView(BaseListView):
    """A view that lists a set of Review objects."""

    base_template = "review/base_list.html"

    title = _("Literature Review")
    help_text = _(
        "The following literature items may contain data that are relevant to this portal but have not yet been added."
        " You can contribute to our community by selecting an item to review, assessing any relevant data, then"
        " submitting a request to add the data to the portal. All contributions will be appropriately acknowledged in"
        " the next major database release. You can find out more about the release cycle of the Global Heat Flow"
        " Database and how your contributions make a difference. "
    )
    template_name = "reviews/literature_list.html"

    filterset_class = ReviewFilter
    queryset = Literature.objects.filter(review__isnull=True).order_by("-created")
