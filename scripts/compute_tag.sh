#!/bin/bash

# Variables
REPO_NAME=$1
AWS_REGION=$2
MAJOR=$3
MINOR=$4

# Fetch all tags from ECR
RAW_TAGS=$(aws ecr list-images --repository-name "$REPO_NAME" --region "$AWS_REGION" --query 'imageIds[].imageTag' --output json | jq -r '.[] | select(. != null and length > 0 and test("'$MAJOR'\\.'$MINOR'\\.[0-9]+$$"))')

# Sort tags and get the latest one
LATEST_TAG=$(echo "$RAW_TAGS" | sort -V | tail -n 1)

# Compute the new patch version
if [ -n "$LATEST_TAG" ]; then
    PATCH=$(echo "$LATEST_TAG" | cut -d. -f3 | awk '{print $1 + 1}')
else
    PATCH=1
fi

# Construct the new image tag
IMAGE_TAG="$MAJOR.$MINOR.$PATCH"

# Output the results for debugging
echo "RAW_TAGS: $RAW_TAGS"
echo "LATEST_TAG: $LATEST_TAG"
echo "PATCH: $PATCH"
echo "IMAGE_TAG: $IMAGE_TAG"

# Export IMAGE_TAG for use in Makefile
echo "export IMAGE_TAG=$IMAGE_TAG" > .image_tag
