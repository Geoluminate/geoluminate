import json

import boto3
from botocore.exceptions import ClientError
from django.conf import settings


def create_bucket(bucket_name):
    # Initialize a Boto3 session
    session = boto3.session.Session()

    # Create a client with the MinIO server endpoint
    s3_client = session.client(
        service_name="s3",
        endpoint_url=settings.AWS_S3_ENDPOINT_URL,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name="us-east-1",  # Use a valid region name
    )

    # Create the bucket
    try:
        s3_client.create_bucket(Bucket=bucket_name)
        print(f'Bucket "{bucket_name}" created successfully.')
    except ClientError as e:
        if e.response["Error"]["Code"] == "BucketAlreadyExists":
            print(f'Bucket "{bucket_name}" already exists.')
        elif e.response["Error"]["Code"] == "BucketAlreadyOwnedByYou":
            print(f'Bucket "{bucket_name}" already owned by you.')
        else:
            print(f"Error occurred: {e}")

    set_bucket_policy(bucket_name)


def set_bucket_policy(bucket_name):
    # Define the bucket policy
    bucket_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {"Effect": "Allow", "Principal": "*", "Action": "s3:GetObject", "Resource": f"arn:aws:s3:::{bucket_name}/*"}
        ],
    }

    # Initialize a Boto3 session
    session = boto3.session.Session()

    # Create a client with the MinIO server endpoint
    s3_client = session.client(
        service_name="s3",
        endpoint_url=settings.AWS_S3_ENDPOINT_URL,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name="us-east-1",  # Use a valid region name
    )

    # Set the bucket policy
    try:
        s3_client.put_bucket_policy(Bucket=bucket_name, Policy=json.dumps(bucket_policy))
        print(f'Policy applied to bucket "{bucket_name}".')
    except ClientError as e:
        print(f"Error occurred while setting policy: {e}")
