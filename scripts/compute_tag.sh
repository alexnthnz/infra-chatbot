#!/bin/bash

# Variables
REPO_NAME=$1
AWS_REGION=$2
MAJOR=$3
MINOR=$4

# Validate inputs
if [ -z "$REPO_NAME" ] || [ -z "$AWS_REGION" ] || [ -z "$MAJOR" ] || [ -z "$MINOR" ]; then
    echo "Error: All arguments (REPO_NAME, AWS_REGION, MAJOR, MINOR) must be provided" >&2
    exit 1
fi

# Validate AWS_REGION format
if ! echo "$AWS_REGION" | grep -Eq '^[a-z]{2}-[a-z]+-[0-9]+$'; then
    echo "Error: Invalid AWS_REGION format: $AWS_REGION" >&2
    exit 1
fi

# Fetch all tags from ECR
RAW_TAGS=$(aws ecr list-images --repository-name "$REPO_NAME" --region "$AWS_REGION" --query 'imageIds[].imageTag' --output json 2>/dev/null | jq -r '.[] | select(. != null and length > 0 and test("'$MAJOR'\\.'$MINOR'\\.[0-9]+$$"))')

# Check if AWS command failed
if [ $? -ne 0 ]; then
    echo "Error: Failed to fetch tags from ECR for $REPO_NAME in $AWS_REGION" >&2
    exit 1
fi

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

# Output the tag
echo "$IMAGE_TAG"
