GEOLUMINATE_LABELS = {
    "project": {"verbose_name": "Project", "verbose_name_plural": "Projects"},
    "dataset": {"verbose_name": "Dataset", "verbose_name_plural": "Datasets"},
    "sample": {"verbose_name": "Sample", "verbose_name_plural": "Samples"},
}

GEOLUMINATE_ALLOWED_IDENTIFIERS = {
    "samples.Sample": {
        "IGSN": "https://igsn.org/",
        # "DOI": "https://doi.org/",
    },
    "contributors.Person": {
        "ORCID": "https://orcid.org/",
        # "researcher_id": "https://app.geosamples.org/sample/researcher_id/",
        # "scopus_id": "https://app.geosamples.org/sample/scopus_id/",
        # "researchgate_id": "https://app.geosamples.org/sample/researchgate_id/",
    },
    "contributors.Organization": {
        "ROR": "https://ror.org/",
        "GRID": "https://www.grid.ac/institutes/",
        "Wikidata": "https://www.wikidata.org/wiki/",
        "ISNI": "https://isni.org/isni/",
        "Crossref Funder ID": "https://doi.org/",
    },
}


GEOLUMINATE_LOCATION = {
    "x": {
        "decimal_places": 6,
    },
    "y": {
        "decimal_places": 6,
    },
}
