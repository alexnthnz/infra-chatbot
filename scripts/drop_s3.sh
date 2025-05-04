#!/bin/bash

# Variables
AWS_REGION="ap-southeast-2"

# Check for bucket name argument
if [ -z "$1" ]; then
  echo "Error: Bucket name must be provided as an argument."
  exit 1
fi
BUCKET_NAME="$1"

# Function to check if an S3 bucket exists
check_s3_bucket() {
  local bucket=$1
  if aws s3 ls s3://$bucket --region $AWS_REGION >/dev/null 2>&1; then
    return 0  # Bucket exists
  else
    return 1  # Bucket does not exist
  fi
}

# Clear and Delete S3 Bucket
if check_s3_bucket "$BUCKET_NAME"; then
  echo "Clearing all items from S3 bucket: $BUCKET_NAME"
  aws s3 rm s3://$BUCKET_NAME --recursive --region $AWS_REGION || { echo "Failed to clear $BUCKET_NAME"; exit 1; }
  echo "Deleting S3 bucket: $BUCKET_NAME"
  aws s3 rb s3://$BUCKET_NAME --force --region $AWS_REGION || { echo "Failed to delete $BUCKET_NAME"; exit 1; }
else
  echo "S3 bucket $BUCKET_NAME does not exist, skipping deletion."
fi

echo "S3 bucket cleanup completed successfully!"
