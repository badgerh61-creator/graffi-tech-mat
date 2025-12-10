import boto3
from botocore.client import Config
from ..core.config import settings

def get_s3_client():
    kwargs = {}
    if settings.S3_ENDPOINT_URL:
        kwargs['endpoint_url'] = settings.S3_ENDPOINT_URL
    if settings.AWS_REGION:
        kwargs.setdefault('region_name', settings.AWS_REGION)
    client = boto3.client('s3', config=Config(signature_version='s3v4'), **kwargs)
    return client

def upload_fileobj(fileobj, key, content_type=None):
    client = get_s3_client()
    extra = {}
    if content_type:
        extra['ContentType'] = content_type
    client.upload_fileobj(fileobj, settings.S3_BUCKET, key, ExtraArgs=extra)
    return key

def create_presigned_post(key, expires_in=3600):
    client = get_s3_client()
    bucket = settings.S3_BUCKET
    fields = {'key': key}
    conditions = [{'bucket': bucket}, {'key': key}]
    return client.generate_presigned_post(Bucket=bucket, Key=key, ExpiresIn=expires_in, Fields=fields, Conditions=conditions)

def get_object_url(key):
    client = get_s3_client()
    endpoint = client.meta.endpoint_url or f"https://{settings.S3_BUCKET}.s3.amazonaws.com"
    if endpoint and settings.S3_BUCKET in endpoint:
        return f"{endpoint.rstrip('/')}/{key}"
    return f"https://{settings.S3_BUCKET}.s3.amazonaws.com/{key}"
