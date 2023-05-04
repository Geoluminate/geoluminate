import os

STATIC_URL = "/static/"
""""""
MEDIA_URL = "/media/"
""""""

# DJANGO_STORAGES SETTINGS
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
""""""
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
""""""
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_BUCKET_NAME")
""""""
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
""""""
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",
}
""""""
AWS_S3_REGION_NAME = os.environ.get("REGION_NAME")
""""""
# 'ap-southeast-2'


AWS_DEFAULT_ACL = None
""""""

AWS_STATIC_LOCATION = "static"
""""""

AWS_PUBLIC_MEDIA_LOCATION = "media/public"
""""""

AWS_PRIVATE_MEDIA_LOCATION = "media/private"
""""""
