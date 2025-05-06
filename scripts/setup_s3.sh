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
    echo "S3 bucket $bucket already exists."
    return 0  # Bucket exists
  else
    echo "S3 bucket $bucket does not exist."
    return 1  # Bucket does not exist
  fi
}

# Create S3 Bucket
if ! check_s3_bucket "$BUCKET_NAME"; then
  echo "Creating S3 bucket: $BUCKET_NAME"
  aws s3 mb s3://$BUCKET_NAME --region $AWS_REGION || { echo "Failed to create $BUCKET_NAME"; exit 1; }
else
  echo "Skipping creation of $BUCKET_NAME as it already exists."
fi

# Output the bucket name for reference
echo "S3 bucket: $BUCKET_NAME"
