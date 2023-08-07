from contextlib import contextmanager
from botocore.exceptions import ClientError
import os
import logging

# Use a context manager to help handle setup/teardown automatically before/after tests are run
@contextmanager
def s3_setup(s3_client, bucket_name):
    s3_client.create_bucket(Bucket=bucket_name)
    yield

def list_buckets(s3_client):
    response = s3_client.list_buckets()
    return [bucket["Name"] for bucket in response["Buckets"]]

def list_objects(s3_client, bucket_name):
    response = s3_client.list_objects_v2(
        Bucket=bucket_name,
    )
    return response
    #return [object["Key"] for object in response["Contents"]]

def upload_file(s3_client, file_name, bucket, key=None):
    # If S3 key was not specified, use file_name
    if key is None:
        key = os.path.basename(file_name)

    try:
        response = s3_client.upload_file(file_name, bucket, key)
    except ClientError as e:
        logging.error(e)
        return False

    return True

# Buckets
def EcomWebassetsDev(s3_client):
    bucket_name = 'ecom-webassets-dev'
    with s3_setup(s3_client, bucket_name):
        return True