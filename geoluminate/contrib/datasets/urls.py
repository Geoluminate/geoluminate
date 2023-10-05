from django.urls import include, path
from django.views.generic import TemplateView

# from .views.account import AccountEmailView
from .views import AddDescription, DatasetEdit, EditDescription

app_name = "dataset"
urlpatterns = [
    path("datasets/<uuid:uuid>/descriptions/", EditDescription.as_view(), name="dataset-description-edit"),
    path("datasets/<uuid:uuid>/", DatasetEdit.as_view(name="dataset-edit", extra_context={"edit": True})),
    path("datasets/<uuid:uuid>/descriptions/add/", AddDescription.as_view(), name="dataset-description-add"),
]
