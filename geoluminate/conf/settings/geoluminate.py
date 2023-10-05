from django.utils.translation import gettext_lazy as _

GEOLUMINATE_SAMPLE_TYPES = ["location", "soil", "water", "plant", "other"]

# must exist in GEOLUMINATE_SAMPLE_TYPES
GEOLUMINATE_DEFAULT_SAMPLE_TYPE = "location"

GEOLUMINATE_IDENTIFIER_SCHEMES = {
    # "ROR": {"URI": "https://ror.org/{identifier}"},
    # "ORCID": {"URI": "https://orcid.org/{identifier}"},
    # "GRID": {"URI": "https://www.grid.ac/institutes/{identifier}"},
    # "Wikidata": {"URI": "https://www.wikidata.org/wiki/{identifier}"},
    # "ISNI": {"URI": "https://isni.org/isni/{identifier}"},
    # "Crossref Funder ID": {"URI": "https://doi.org/{identifier}"},
    # "DOI": {"URI": "https://doi.org/{identifier}"},
    # "IGSN": {"URI": "https://app.geosamples.org/sample/igsn/{identifier}"},
    # "researcher_id": {"URI": "https://app.geosamples.org/sample/researcher_id/{identifier}"},
    # "scopus_id": {"URI": "https://app.geosamples.org/sample/scopus_id/{identifier}"},
    # "researchgate_id": {"URI": "https://app.geosamples.org/sample/researchgate_id/{identifier}"},
}

GEOLUMINATE_ALLOWED_IDENTIFIERS = {
    "contributors.Contributor": ["orcid", "researcher_id", "scopus_id", "researchgate_id"],
    # "projects.Project": ["doi"],
    "samples.Sample": ["IGSN"],
    "datasets.Dataset": ["DOI"],
    # organization IDs from https://ror.readme.io/docs/ror-data-structure#external_ids
    "organization.Organization": ["ROR", "GRID", "Wikidata", "ISNI", "Crossref Funder ID"],
    "literature.Literature": ["DOI"],
}

GEOLUMINATE_SUBMISSION_APPROVAL = "manual"
"Valid options are: 'manual', 'automatic', 'both' or 'none'"


GEOLUMINATE_SUBMISSION_APPROVAL_METHOD = ""
"""A dotted path to a function that will be called to approve a submission. Only applicable when
GEOLUMINATE_SUBMISSION_APPROVAL is 'automatic' or 'both'"""
# maybe this requires a method on each measurement Model that returns a boolean?

GEOLUMINATE_NAVBAR_WIDGETS = [
    "geoluminate/widgets/user_navbar_widget.html",
]
"""A list of widget templates to render to the right side of the main navbar."""

GEOLUMINATE_USER_SIDEBAR_WIDGETS = [
    "geoluminate/widgets/theme_toggle.html",
]
"""A list of widget templates to render below the user display name in the user sidebar."""


GEOLUMINATE_PROJECT_PAGES = [
    ("fas fa-circle-info", _("About"), "core/pages/descriptions.html"),
    ("fas fa-users", _("Contributors"), "core/pages/contributors.html"),
    ("fas fa-timeline", _("Timeline"), "core/pages/timeline.html"),
    ("fas fa-map-location-dot", _("Map"), "geoluminate/components/map.html"),
    ("fas fa-comments", _("Discussion"), "core/pages/discussion.html"),
    ("fas fa-paperclip", _("Attachments"), "core/pages/attachments.html"),
    ("fas fa-folder-open", _("Datasets"), "core/pages/datasets.html"),
]

GEOLUMINATE_DATASET_PAGES = [
    ("fas fa-circle-info", _("About"), "core/pages/descriptions.html"),
    ("fas fa-users", _("Contributors"), "core/pages/contributors.html"),
    ("fas fa-timeline", _("Timeline"), "core/pages/timeline.html"),
    ("fas fa-map-location-dot", _("Map"), "geoluminate/components/map.html"),
    ("fas fa-comments", _("Discussion"), "core/pages/discussion.html"),
    ("fas fa-paperclip", _("Attachments"), "core/pages/attachments.html"),
    ("fas fa-database", _("Samples"), "core/pages/samples.html"),
]

GEOLUMINATE_DESCRIPTION_TYPES = {
    "core.Dataset": "geoluminate.contrib.core.choices.DataCiteDescriptionTypes",
    "core.Project": "geoluminate.contrib.core.choices.DataCiteDescriptionTypes",
    "core.Sample": "geoluminate.contrib.core.choices.DataCiteDescriptionTypes",
}
