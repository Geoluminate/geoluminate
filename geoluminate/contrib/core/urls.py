from django.urls import include, path, re_path
from django.utils.text import slugify
from django.views.generic import TemplateView

from geoluminate.utils import get_measurement_models

from . import views

urlpatterns = [
    re_path(r"^update/(?P<content_type_id>[^/]+)/(?P<object_id>[^/]+)/", views.update_object, name="update_object"),
    path(
        "activity/",
        include(
            [
                re_path(
                    r"^follow/(?P<content_type_id>[^/]+)/(?P<object_id>[^/]+)/(?:(?P<flag>[^/]+)/)?$",
                    views.follow_unfollow,
                    name="actstream_follow",
                ),
                re_path(
                    r"^follow_all/(?P<content_type_id>[^/]+)/(?P<object_id>[^/]+)/(?:(?P<flag>[^/]+)/)?$",
                    views.follow_unfollow,
                    {"actor_only": False},
                    name="actstream_follow_all",
                ),
                re_path(
                    r"^unfollow_all/(?P<content_type_id>[^/]+)/(?P<object_id>[^/]+)/(?:(?P<flag>[^/]+)/)?$",
                    views.follow_unfollow,
                    {"actor_only": False, "do_follow": False},
                    name="actstream_unfollow_all",
                ),
                re_path(
                    r"^unfollow/(?P<content_type_id>[^/]+)/(?P<object_id>[^/]+)/(?:(?P<flag>[^/]+)/)?$",
                    views.follow_unfollow,
                    {"do_follow": False},
                    name="actstream_unfollow",
                ),
            ]
        ),
    ),
    path(
        "<object_type>/<uuid:uuid>/",
        include(
            [
                path("contact/", views.GenericContactForm.as_view(), name="contact"),
                path(
                    "description/add/",
                    views.DescriptionCreateView.as_view(),
                    name="description-add",
                ),
                path("description/<dtype>/", views.DescriptionDetailView.as_view(), name="description-detail"),
                path(
                    "description/<dtype>/update/",
                    views.DescriptionUpdateView.as_view(),
                    name="description-edit",
                ),
                path("description/<dtype>/delete/", views.DescriptionDeleteView.as_view(), name="description-edit"),
            ]
        ),
    ),
]
patterns = []
for model in get_measurement_models():
    app = model._meta.app_label
    name = model._meta.model_name
    route = f"{slugify(app)}/{slugify(name)}/"

    patterns.append(path(route, TemplateView.as_view(), name=f"{app}_{name}"))


# app_name = "core"
urlpatterns.append(path("measurements/", include(patterns)))
