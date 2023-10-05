from django.urls import include, path
from django.views.generic import TemplateView

# from .views.account import AccountEmailView
from .views import AddProjectView, ProjectDetail

app_name = "project"
urlpatterns = [
    path("projects/<uuid:uuid>/", ProjectDetail.as_view(extra_context={"edit": True}, name="project-edit")),
    path("new/project/", AddProjectView.as_view(), name="project-add"),
]
