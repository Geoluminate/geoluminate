# EASY_THUMBNAILS SETTINGS
THUMBNAIL_CACHE_DIMENSIONS = True
""""""

# THUMBNAIL_CHECK_CACHE_MISS = True
THUMBNAIL_SUBDIR = "thumbs"
""""""

THUMBNAIL_ALIASES = {
    "contributors.Person": {
        "thumb": {"size": (48, 48), "crop": False},
    },
}
""""""

THUMBNAIL_PROCESSORS = [
    "easy_thumbnails.processors.colorspace",
    "easy_thumbnails.processors.autocrop",
    "easy_thumbnails.processors.scale_and_crop",
    # "filer.thumbnail_processors.scale_and_crop_with_subject_location",
    "easy_thumbnails.processors.filters",
]
""""""

THUMBNAIL_DEBUG = True
""""""
