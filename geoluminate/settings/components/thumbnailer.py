WATERMARK = dict(
                image='collection/images/logo_square.png',
                position='50%x70%',
                opacity=0.7,
                scale='15%',
                )

# EASY_THUMBNAILS SETTINGS
THUMBNAIL_CACHE_DIMENSIONS = True
# THUMBNAIL_CHECK_CACHE_MISS = True
THUMBNAIL_SUBDIR = 'thumbs'
THUMBNAIL_ALIASES = {}
# THUMBNAIL_NAMER = 'easy_thumbnails.namers.alias'
THUMBNAIL_PROCESSORS = [
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters',
]

THUMBNAIL_DEBUG = True
