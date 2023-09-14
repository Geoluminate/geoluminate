GEOLUMINATE_SAMPLE_TYPES = ["location", "soil", "water", "plant", "other"]

# must exist in GEOLUMINATE_SAMPLE_TYPES
GEOLUMINATE_DEFAULT_SAMPLE_TYPE = "location"

GEOLUMINATE_ALLOWED_IDENTIFIERS = {
    "user.Contributor": ["orcid", "researcher_id", "scopus_id", "researchgate_id"],
    "project.Project": ["doi"],
    "project.Sample": ["IGSN"],
    "project.Dataset": ["doi"],
    "literature.Literature": ["doi"],
}
