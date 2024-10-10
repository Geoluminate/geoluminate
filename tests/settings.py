import geoluminate

geoluminate.setup(
    apps=[
        "example",
        "django_better_admin_arrayfield",
    ]
)

ROOT_URLCONF = "geoluminate.urls"
