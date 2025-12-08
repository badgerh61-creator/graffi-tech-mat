import boto3
from app.core.config import settings

def get_s3_client():
    return boto3.client(
        "s3",
        endpoint_url=settings.S3_ENDPOINT,
        aws_access_key_id=settings.S3_ACCESS_KEY,
        aws_secret_access_key=settings.S3_SECRET_KEY,
        region_name="us-east-1",
    )


def upload_bytes(key: str, data: bytes, content_type="application/octet-stream"):
    s3 = get_s3_client()
    s3.put_object(
        Bucket=settings.S3_BUCKET,
        Key=key,
        Body=data,
        ContentType=content_type
    )
    return build_public_url(key)


def build_public_url(key: str):
    endpoint = settings.S3_ENDPOINT.rstrip("/")
    return f"{endpoint}/{settings.S3_BUCKET}/{key}"
