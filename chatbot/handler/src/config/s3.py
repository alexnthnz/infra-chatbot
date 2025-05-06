import boto3
from botocore.exceptions import ClientError
from fastapi import HTTPException, UploadFile

from config.config import config  # Import the config object

# Initialize S3 client using config values
s3_client = boto3.client(
    "s3",
    aws_access_key_id=config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
    region_name=config.AWS_REGION,
)


def upload_to_s3(file: UploadFile, folder: str = "uploads", expires_in: int = 3600) -> str:
    """
    Upload a file to a private S3 bucket and return a presigned URL for access.

    Args:
        file (UploadFile): The file to upload (from FastAPI).
        folder (str): The S3 folder/prefix to store the file in (default: "uploads").
        expires_in (int): Expiration time in seconds for the presigned URL (default: 1 hour).

    Returns:
        str: A presigned URL for temporary access to the uploaded file.

    Raises:
        HTTPException: If the upload or URL generation fails.
    """
    try:
        # Generate a unique key (e.g., uploads/filename)
        file_key = f"{folder}/{file.filename}"

        # Upload the file to the private bucket
        s3_client.upload_fileobj(
            file.file,  # File object from UploadFile
            config.AWS_S3_BUCKET,
            file_key,
            ExtraArgs={"ContentType": file.content_type},  # Set MIME type
        )

        # Generate a presigned URL for temporary access
        file_url = s3_client.generate_presigned_url(
            "get_object", Params={"Bucket": config.AWS_S3_BUCKET, "Key": file_key}, ExpiresIn=expires_in
        )
        return file_url

    except ClientError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to upload file to S3 or generate presigned URL: {str(e)}",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error during S3 upload: {str(e)}")


def get_s3_client() -> boto3.client:
    """
    Return the configured S3 client for advanced usage if needed.
    """
    return s3_client


def generate_presigned_url(file_key: str, expires_in: int = 3600) -> str:
    """
    Generate a presigned URL for an existing S3 object.

    Args:
        file_key (str): The S3 key of the file (e.g., "uploads/filename.jpg").
        expires_in (int): Expiration time in seconds (default: 1 hour).

    Returns:
        str: A presigned URL for temporary access.
    """
    try:
        url = s3_client.generate_presigned_url(
            "get_object", Params={"Bucket": config.AWS_S3_BUCKET, "Key": file_key}, ExpiresIn=expires_in
        )
        return url
    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate presigned URL: {str(e)}")
