# a list of dotted paths to vocabularies that can be tagged on a model
GEOLUMINATE_TAGGABLE_CONCEPTS = []


# must exist in GEOLUMINATE_SAMPLE_TYPES
GEOLUMINATE_DEFAULT_FEATURE_TYPE = "site"


GEOLUMINATE_LABELS = {
    "project": {"verbose_name": "Project", "verbose_name_plural": "Projects"},
    "dataset": {"verbose_name": "Dataset", "verbose_name_plural": "Datasets"},
    "sample": {"verbose_name": "Sample", "verbose_name_plural": "Samples"},
}

IdentifierSchemes = {
    "ARK": "https://n2t.net/ark:/",
    "arXiv": "https://arxiv.org/",
    "bibcode": "https://ui.adsabs.harvard.edu/",
    "DOI": "https://doi.org/",
    "EAN13": "https://www.ean-search.org/",
    "EISSN": "https://www.issn.org/",
    "Handle": "https://hdl.handle.net/",
    "IGSN": "https://igsn.org/",
    "ISBN": "https://www.isbn-international.org/",
    "ISSN": "https://www.issn.org/",
    "ISTC": "https://www.istc-international.org/",
    "LISSN": "https://www.issn.org/",
    "LSID": "https://www.lsid.info/",
    "PMID": "https://www.ncbi.nlm.nih.gov/",
    "PURL": "https://archive.org/services/purl/",
    "UPC": "https://www.ean-search.org/",
    "URL": "https://www.iana.org/",
    "URN": "https://www.iana.org/",
}


GEOLUMINATE_ALLOWED_IDENTIFIERS = {
    "geoluminate.Sample": {
        "IGSN": "https://igsn.org/",
        # "DOI": "https://doi.org/",
    },
    "literature.Literature": {
        "DOI": "https://doi.org/",
        "ISBN": "https://www.isbn-international.org/",
        "ISSN": "https://www.issn.org/",
        "URL": "https://www.iana.org/",
    },
    "geoluminate.Dataset": {
        "ARK": "https://n2t.net/ark:/",
        "arXiv": "https://arxiv.org/",
        "bibcode": "https://ui.adsabs.harvard.edu/",
        "DOI": "https://doi.org/",
        "EAN13": "https://www.ean-search.org/",
        "EISSN": "https://www.issn.org/",
        "Handle": "https://hdl.handle.net/",
        "ISTC": "https://www.istc-international.org/",
        "LISSN": "https://www.issn.org/",
        "LSID": "https://www.lsid.info/",
        "PMID": "https://www.ncbi.nlm.nih.gov/",
        "PURL": "https://archive.org/services/purl/",
        "UPC": "https://www.ean-search.org/",
        "URL": "https://www.iana.org/",
        "URN": "https://www.iana.org/",
    },
    # "contributors.Personal": {
    #     "ORCID": "https://orcid.org/",
    #     # "researcher_id": "https://app.geosamples.org/sample/researcher_id/",
    #     # "scopus_id": "https://app.geosamples.org/sample/scopus_id/",
    #     # "researchgate_id": "https://app.geosamples.org/sample/researchgate_id/",
    # },
    "contributors.Organization": {
        "ROR": "https://ror.org/",
        "GRID": "https://www.grid.ac/institutes/",
        "Wikidata": "https://www.wikidata.org/wiki/",
        "ISNI": "https://isni.org/isni/",
        "Crossref Funder ID": "https://doi.org/",
    },
}

GEOLUMINATE_SUBMISSION_APPROVAL = "manual"
"Valid options are: 'manual', 'automatic', 'both' or 'none'"


GEOLUMINATE_SUBMISSION_APPROVAL_METHOD = ""
"""A dotted path to a function that will be called to approve a submission. Only applicable when
GEOLUMINATE_SUBMISSION_APPROVAL is 'automatic' or 'both'"""
# maybe this requires a method on each measurement Model that returns a boolean?

GEOLUMINATE_NAVBAR_WIDGETS = [
    "geoluminate/navigation/widgets/page_edit_toggle.html",
    "geoluminate/navigation/widgets/admin_link.html",
    "geoluminate/navigation/widgets/theme_toggle.html",
    "geoluminate/navigation/widgets/user_navigation.html",
]
"""A list of widget templates to render to the right side of the main navbar."""

GEOLUMINATE_USER_SIDEBAR_WIDGETS = [
    # "geoluminate/widgets/admin_link.html",
    # "geoluminate/widgets/theme_toggle.html",
]
"""A list of widget templates to render below the user display name in the user sidebar."""


GEOLUMINATE_DESCRIPTION_TYPES = {
    "core.Dataset": "geoluminate.contrib.datasets.choices.DataCiteDescriptionTypes",
    "core.Project": "geoluminate.contrib.datasets.choices.DataCiteDescriptionTypes",
    "core.Sample": "geoluminate.contrib.datasets.choices.DataCiteDescriptionTypes",
}

GEOLUMINATE_FILTERS = {
    "geoluminate.Dataset": {
        "title": ["contains"],
        "keywords__name": ["exact"],
    }
}


GEOLUMINATE_ICONS = {
    "project": "fa-solid fa-project-diagram",
    "dataset": "fa-solid fa-folder-open",
    "sample": "fa-solid fa-database",
    "person": "fa-solid fa-user",
    "organization": "fa-solid fa-institution",
    "location": "fa-solid fa-map-marker-alt",
    "measurement": "fa-solid fa-flask",
    "map": "fa-solid fa-map-location-dot",
    "timeline": "fa-solid fa-bars-staggered",
    "contributors": "fa-solid fa-users",
    "overview": "fa-solid fa-book-open",
    "activity": "fa-solid fa-rss fa-rotate-270",
    "review": "fa-solid fa-magnifying-glass-chart",
    "discussion": "fa-solid fa-comments",
    "plus": "fa-solid fa-plus",
    "spinner": "fa-solid fa-spinner fa-spin",
    "literature": "fa-solid fa-book",
}
