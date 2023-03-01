"""
A collection of classes for handling the storage of files on a remote
server. Currently available classes are setup to work with Amazon S3 and
are subclassed from the `S3Boto3Storage`, `S3StaticStorage` of `django_storages`.
"""
from django.conf import settings
from storages.backends.azure_storage import AzureStorage
from storages.backends.gcloud import GoogleCloudStorage
from storages.backends.s3boto3 import S3Boto3Storage


class S3StaticStorage(S3Boto3Storage):
    """Sets the `default_acl` value to public to ensure no authentication
    is required to access static files."""

    querystring_auth = False
    location = settings.AWS_STATIC_LOCATION
    default_acl = "public-read"


class S3PublicMediaStorage(S3Boto3Storage):
    """Sets the `default_acl` value to public to ensure no authentication
    is required to access public media files."""

    location = settings.AWS_PUBLIC_MEDIA_LOCATION
    file_overwrite = False
    default_acl = "public-read"


class S3PrivateMediaStorage(S3Boto3Storage):
    """Sets the `default_acl` value to private to ensure authentication
    is required to access private media files."""

    location = settings.AWS_PRIVATE_MEDIA_LOCATION
    default_acl = "private"
    file_overwrite = False
    custom_domain = False


class GoogleCloudStaticStorage(GoogleCloudStorage):
    location = "static"
    default_acl = "publicRead"


class GoogleCloudMediaStorage(GoogleCloudStorage):
    location = "media"
    file_overwrite = False


class AzureStaticStorage(AzureStorage):
    location = "static"


class AzureMediaStorage(AzureStorage):
    location = "media"
    file_overwrite = False
