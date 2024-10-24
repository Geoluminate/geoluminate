from django.urls import include, path, re_path

from .views import generic, literature

urlpatterns = [
    re_path(
        r"^update/(?P<content_type_id>[^/]+)/(?P<object_id>[^/]+)/",
        generic.update_object,
        name="update_object",
    ),
    path(
        "activity/",
        include(
            [
                re_path(
                    r"^follow/(?P<content_type_id>[^/]+)/(?P<object_id>[^/]+)/(?:(?P<flag>[^/]+)/)?$",
                    generic.follow_unfollow,
                    name="actstream_follow",
                ),
                re_path(
                    r"^follow_all/(?P<content_type_id>[^/]+)/(?P<object_id>[^/]+)/(?:(?P<flag>[^/]+)/)?$",
                    generic.follow_unfollow,
                    {"actor_only": False},
                    name="actstream_follow_all",
                ),
                re_path(
                    r"^unfollow_all/(?P<content_type_id>[^/]+)/(?P<object_id>[^/]+)/(?:(?P<flag>[^/]+)/)?$",
                    generic.follow_unfollow,
                    {"actor_only": False, "do_follow": False},
                    name="actstream_unfollow_all",
                ),
                re_path(
                    r"^unfollow/(?P<content_type_id>[^/]+)/(?P<object_id>[^/]+)/(?:(?P<flag>[^/]+)/)?$",
                    generic.follow_unfollow,
                    {"do_follow": False},
                    name="actstream_unfollow",
                ),
            ]
        ),
    ),
    path(
        "create/description/<str:pk>/",
        include(
            [
                path("contact/", generic.GenericContactForm.as_view(), name="contact"),
                path(
                    "description/new/",
                    generic.DescriptionCreateView.as_view(),
                    name="description-create",
                ),
                # path(
                #     "description/<dtype>/",
                #     views.DescriptionDetailView.as_view(),
                #     name="description-detail",
                # ),
                # path(
                #     "description/<dtype>/update/",
                #     views.DescriptionUpdateView.as_view(),
                #     name="description-edit",
                # ),
                # path(
                #     "description/<dtype>/delete/",
                #     views.DescriptionDeleteView.as_view(),
                #     name="description-edit",
                # ),
            ]
        ),
    ),
    path("team/", generic.PortalTeamView.as_view(), name="portal-team"),
    path("references/", literature.ReferenceListView.as_view(), name="reference-list"),
]
