import boto3
from django.conf import settings

def get_s3_client():
    return boto3.client(
        "s3",
        endpoint_url=settings.SUPABASE_STORAGE_URL,
        aws_access_key_id=settings.SUPABASE_ACCESS_KEY,
        aws_secret_access_key=settings.SUPABASE_SECRET_KEY,
        region_name=settings.SUPABASE_REGION,
    )

def public_url_for_key(key: str) -> str:
    base = settings.SUPABASE_PUBLIC_BASE.rstrip("/")
    bucket = settings.SUPABASE_BUCKET
    return f"{base}/storage/v1/object/public/{bucket}/{key}"
