import logging
import os
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError


def get_s3_client():
    """Create a Boto3 client configured for MinIO"""
    return boto3.client(
        's3',
        endpoint_url=os.getenv("MINIO_ENDPOINT", "http://localhost:9000"),
        aws_access_key_id=os.getenv("MINIO_ROOT_USER", "minioadmin"),
        aws_secret_access_key=os.getenv("MINIO_ROOT_PASSWORD", "minioadmin"),
        # MinIO requires s3v4 signature
        config=Config(signature_version='s3v4'),
        region_name="us-east-1"  # Required by boto3 even for local
    )


def create_presigned_url(
    object_name: str, 
    content_type: str, 
    bucket_name: str = None, 
    expiration: int = 3600) -> str:
    """Generate a presigned URL to share an minio/S3 object
    
    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid 
    :return: Presigned URL as string, If error, returns None.
    """
    
    # load bucket from env if not passed
    if bucket_name is None:
        bucket_name = os.getenv("BK_NAME", "taskflow-uploads")
    
    s3_client = get_s3_client()
    try:
        # Generate the URL
        response = s3_client.generate_presigned_url(
            'put_object',
            # PUT for upload, GET for downloads
            Params={
                'Bucket': bucket_name, 
                'Key': object_name,
                'ContentType': content_type},
            ExpiresIn=expiration
        )
        # The response contains the presigned URL
        return response
    except ClientError as e:
        logging.error(e)
        return None
    