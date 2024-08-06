from pathlib import Path

import geoluminate

GEOLUMINATE = {
    "application": {
        "domain": "localhost:8000",
        "developers": [
            {
                "email": "super.user@example.com",
                "name": "Super User",
            },
        ],
    },
    "database": {
        "name": "Geoluminate Example Database",
        "short_name": "Geoluminate",
        "keywords": ["research", "data management", "FAIR data"],
    },
    "governance": {
        "name": "Geoluminate",
        "short_name": "Geoluminate",
        "url": "https://www.geoluminate.net",
        "contact": "support@geoluminate.net",
    },
}


INSTALLED_APPS = [
    "example",
]


BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

geoluminate.setup(development=True)


# INSTALLED_APPS.insert(5, "django.contrib.admindocs")


AWS_USE_SSL = False

WEBPACK_LOADER = {
    "GEOLUMINATE": {
        "CACHE": False,
        "STATS_FILE": BASE_DIR / "assets" / "webpack-stats.json",
        "POLL_INTERVAL": 0.1,
        "IGNORE": [r".+\.hot-update.js", r".+\.map"],
    },
}

ALLOWED_HOSTS = [
    "localhost",
]

# GEOLUMINATE_LABELS["sample"] = {"verbose_name": "Heat Flow Site", "verbose_name_plural": "Heat Flow Site"}
