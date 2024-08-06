from django.contrib import messages

# import LoginRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.utils.translation import gettext as _
from django.views.generic import FormView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import UpdateView
from literature.forms import LiteratureForm
from literature.models import LiteratureItem
from literature.views import LiteratureView
from meta.views import MetadataMixin

from geoluminate.contrib.core.view_mixins import ListPluginMixin
from geoluminate.models import Dataset
from geoluminate.utils import icon
from geoluminate.views import BaseDetailView, BaseEditView, BaseListView, HTMXMixin

from . import utils
from .filters import LiteratureFilter, ReviewFilter
from .forms import (
    AcceptReviewForm,  # LiteratureForm,
    LiteratureFormCollection,
    ReviewStatusForm,
)
from .models import Review


class AcceptLiteratureReview(HTMXMixin, MetadataMixin, SingleObjectMixin, LoginRequiredMixin, FormView):
    """A simple view that asks the user to confirm that they want to accept the review. On accepting, a new Review object is created and the user is redirected to the detail view of the related dataset."""

    model = LiteratureItem
    template_name = "reviews/accept_review_form.html"
    form_class = AcceptReviewForm
    title = _("Begin review")

    def get(self, request, *args, **kwargs):
        """If the review has already been accepted, raise a 404 error. If the review has not been accepted, proceed with the form."""

        self.object = self.get_object()

        # pprint.pprint(model_to_dict(self.object))
        # if review := self.object.review:
        #     if review.status == Review.STATUS_CHOICES.ACCEPTED:
        #         raise Http404(_("This literature item has already been reviewed"))
        #     elif review.status == Review.STATUS_CHOICES.IN_PROGRESS or review.status == Review.STATUS_CHOICES.SUBMITTED:
        #         raise Http404(_("This literature item is currently being reviewed"))

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        # create a new dataset object which will store the reviewed data
        self.object = self.get_object()

        self.dataset = utils.dataset_from_literature(self.object)

        # create a new review object
        self.review = Review.objects.create(
            literature=self.object,
            reviewer=self.request.user,
            dataset=self.dataset,
        )

        # message the user
        messages.add_message(
            self.request,
            messages.INFO,
            _("A new review has been added to your profile."),
        )

        return super().form_valid(form)

    def get_success_url(self):
        return self.review.get_absolute_url()


class AcceptReview(UpdateView):
    """A view that allows an administrator to accept a submitted review into the database.

    The administrator is presented with a summary of the review and asked to confirm that they want to accept it.
    """

    model = Review
    form_class = ReviewStatusForm
    status = None
    success_url = "."

    def get_initial(self):
        return {"status": self.status}

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_invalid(form)

    # def get_success_url(self):
    #     return self.dataset.get_absolute_url()


accept_review = AcceptReview.as_view(status=Review.STATUS_CHOICES.ACCEPTED, template_name="reviews/review_accept.html")
reject_review = AcceptReview.as_view(status=Review.STATUS_CHOICES.IN_PROGRESS)
submit_review = AcceptReview.as_view(status=Review.STATUS_CHOICES.SUBMITTED)


class ReviewEditView(BaseEditView):
    model = LiteratureItem
    form_class = ReviewStatusForm
    title = _("Start review")
    template_name = "reviews/literature_form.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"

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
        return self.dataset.get_absolute_url()


class ReviewListView(BaseListView):
    """A view that lists a set of Review objects."""

    template_name = "reviews/review_list.html"
    filterset_class = ReviewFilter
    queryset = Dataset.objects.filter().order_by("-created")


class ReviewPlugin(ListPluginMixin):
    template_name = "geoluminate/plugins/list_view.html"
    object_template = "reviews/review_card.html"
    title = name = _("Reviews")
    icon = icon("review")
    description = _("The following reviews are associated with the this contributor.")

    def get_queryset(self, *args, **kwargs):
        return self.get_object().reviews.all()


class ReviewDetailView(BaseDetailView):
    base_template = "reviews/review_detail.html"
    model = Review
    sidebar_components = [
        "core/sidebar/basic_info.html",
        # "core/sidebar/keywords.html",
        # "core/sidebar/status.html",
        # "core/sidebar/summary.html",
    ]


class ReviewCheckoutView(BaseEditView):
    """This view is used as a final request to submit supporting documents that were used during the review process. It will be accessible to the reviewer only after the review has been successfully completed and formally accepted into the database."""

    model = Review
    # form_class = SupportingDocumentsForm
    title = _("Submit supporting documents")
    template_name = "reviews/supporting_documents_form.html"

    def get(self, request, *args, **kwargs):
        """Make sure the object status is equal to 'accepted' or redirect to the detail view."""
        self.object = self.get_object()
        if self.object.status == "accepted":
            return super().get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(self.object.get_absolute_url())


class ReviewDataUploadView(ReviewDetailView):
    """A view to handle uploading and verification of submitted data."""

    template_name = "datasets/literature_form.html"


class ReviewLiteratureEdit(HTMXMixin, LiteratureView):
    collection_class = LiteratureFormCollection
    template_name = "literature/literature_form.html"
    title = _("Confirm literature details")
    help_text = _(
        "Please confirm that the details of the chosen literature item are correct to the best of your knowledge"
    )

    def get_object(self):
        return self.get_queryset().get(dataset__review__uuid=self.kwargs.get("pk"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["navigation"] = self.navigation
        context["title"] = self.title
        context["help_text"] = self.help_text
        context["review_object"] = self.object.dataset.review
        return context


class LiteratureReviewListView(BaseListView):
    """A view that lists a set of Review objects."""

    base_template = "reviews/review_list.html"
    object_template = "literature/literature_card.html"
    title = _("Data extraction and review")

    filterset_class = ReviewFilter
    queryset = LiteratureItem.objects.order_by("-created")
    # queryset = LiteratureItem.objects.exclude(
    #     review__status=Review.STATUS_CHOICES.ACCEPTED,
    # ).order_by("-created")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total"] = LiteratureItem.objects.count()
        summary = {}
        for item in Review.objects.values("status").annotate(total=Count("status")):
            label = Review.STATUS_CHOICES(item["status"]).label
            summary[label] = {
                "count": item["total"],
                "percent": item["total"] / context["total"] * 100,
            }

        context["summary"] = summary
        return context


class LiteratureListView(BaseListView):
    model = LiteratureItem
    title = _("Literature")
    # base_template = "literature/literature_list.html"
    object_template = "literature/literature_card.html"
    queryset = LiteratureItem.objects.order_by("-created")
    # queryset = LiteratureItem.objects.filter(review__status=Review.STATUS_CHOICES.ACCEPTED).order_by("-created")
    filterset_class = LiteratureFilter
    list_filter_top = ["title", "o"]


class LiteratureEditView(BaseEditView):
    model = LiteratureItem
    title = _("Create a new project")
    help_text = None
    form_class = LiteratureForm
