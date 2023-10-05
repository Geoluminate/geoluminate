from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from formset.views import EditCollectionView
from literature.models import Literature

from geoluminate.contrib.core.views import (
    BaseDetailView,
    CoreListView,
    DescriptionFormView,
    GenericCreateView,
    HTMXBase,
    HTMXMixin,
)

from .forms import DatasetFormCollection, LiteratureForm
from .models import Dataset, Review


class DatasetListView(CoreListView):
    model = Dataset


list_view = DatasetListView.as_view()


class DatasetDetail(BaseDetailView):
    base_template = "base_detail_view.html"
    model = Dataset
    navigation = settings.GEOLUMINATE_DATASET_PAGES


class DatasetEdit(LoginRequiredMixin, DatasetDetail):
    pass


class AddDescription(HTMXMixin, DescriptionFormView):
    base_template = "base_create_view.html"
    slug_field = "uuid"
    slug_url_kwarg = "uuid"
    model = Dataset


class EditDescription(HTMXBase, EditCollectionView):
    base_template = "base_create_view.html"
    slug_field = "uuid"
    slug_url_kwarg = "uuid"
    model = Dataset
    collection_class = DatasetFormCollection
    template_name = "core/base_form_collection.html"
    success_url = reverse_lazy("dataset-list")

    def get_success_url(self):
        return self.request.path

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        if self.object:
            context_data["edit"] = True
            print("Edit")
        else:
            context_data["add"] = True
            print("Add")
        return context_data

    # def form_collection_valid(self, form_collection):

    #     with transaction.atomic():
    #         form_collection.construct_instance(self.object)
    #     # integrity errors may occur during construction, hence revalidate collection
    #     if form_collection.is_valid():
    #         print("Valid")
    #         return super().form_collection_valid(form_collection)
    #     else:
    #         pprint.pprint(form_collection.errors)
    #         return self.form_collection_invalid(form_collection)


class AddDatasetView(EditCollectionView):
    slug_field = "uuid"
    slug_url_kwarg = "uuid"
    model = Dataset
    collection_class = DatasetFormCollection
    template_name = "core/base_form_collection.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        if self.object:
            context_data["edit"] = True
        else:
            context_data["add"] = True
        return context_data

    def get_object(self, queryset=None):
        if self.kwargs.get("uuid"):
            print("Here")
            return self.model.objects.get(uuid=self.kwargs["uuid"])
        print("There")
        return self.model()

    def get_success_url(self):
        model_name = self.object._meta.model.__name__.lower()
        return reverse(f"{model_name}-edit", kwargs={"uuid": self.object.uuid})


# class GenericCreateView(LoginRequiredMixin, HTMXMixin, FormView, CreateView):
#     base_template = "base_create_view.html"
#     template_name = "core/base_form.html"


class ReviewListView(CoreListView):
    model = Review


class ReviewDetail(BaseDetailView):
    model = Review
    navigation = settings.GEOLUMINATE_PROJECT_PAGES


class AddReviewView(GenericCreateView):
    model = Literature
    form_class = LiteratureForm
    title = _("Start a new review")
    help_text = _(
        f"You're about to start a new review for the {settings.GEOLUMINATE['database']['name']}. Reviews are a way for"
        " community members to contribute existing data to the repository without claiming ownership of that data."
        " Make sure you have the right to contribute the data you are about to add. If you are the owner of the data,"
        " consider adding it as a dataset instead."
    )

    def form_valid(self, form):
        # pprint.pprint(form.cleaned_data)
        self.dataset = Dataset()
        response = super().form_valid(form)
        self.dataset.title = self.object.title
        self.dataset.reference = self.object
        self.dataset.save()
        self.review = self.create_review()
        # pprint.pprint(model_to_dict(self.object))
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
        model_name = self.dataset._meta.model.__name__.lower()
        return reverse(f"{model_name}-edit", kwargs={"uuid": self.dataset.uuid})


# class AddReviewView(LoginRequiredMixin, HTMXBase, FormCollectionView):
#     base_template = "base_create_view.html"
#     template_name = "core/review_form.html"
#     model = Literature
#     collection_class = StartNewReviewForm
#     # form_class = StartNewReviewForm
#     title = _("Start a new review")
#     help_text = _("You are about to start a new review to add an existing dataset to this online repository.")

#     def form_valid(self, form):
#         # pprint.pprint(form.cleaned_data)
#         response = super().form_valid(form)
#         self.dataset = self.create_dataset()
#         self.review = self.create_review()
#         # pprint.pprint(model_to_dict(self.object))
#         return response

#     def create_dataset(self):
#         dataset = Dataset.objects.create(
#             title=self.object.title,
#             reference=self.object,
#         )
#         dataset.save()
#         return dataset

#     def create_review(self):
#         review = Review.objects.create(
#             dataset=self.dataset,
#             reviewer=self.request.user,
#         )
#         review.save()
#         return review

#     def get_success_url(self):
#         model_name = self.dataset._meta.model.__name__.lower()
#         return reverse(f"{model_name}-edit", kwargs={"uuid": self.dataset.uuid})
#         # return self.request.path


# class AddReviewView(EditCollectionView):
#     slug_field = "uuid"
#     slug_url_kwarg = "uuid"
#     model = Review
#     collection_class = ProjectFormCollection
#     template_name = "core/base_form_collection.html"

#     def get_context_data(self, **kwargs):
#         context_data = super().get_context_data(**kwargs)
#         if self.object:
#             context_data["edit"] = True
#         else:
#             context_data["add"] = True
#         return context_data

#     def get_object(self, queryset=None):
#         if self.kwargs.get("uuid"):
#             return self.model.objects.get(uuid=self.kwargs["uuid"])
#         return self.model()

#     def get_success_url(self):
#         model_name = self.object._meta.model.__name__.lower()
#         return reverse(f"{model_name}-edit", kwargs={"uuid": self.object.uuid})


list_view = ReviewListView.as_view()
