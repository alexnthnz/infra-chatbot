#!/bin/bash

# Check for repository name and region arguments
if [ -z "$1" ] || [ -z "$2" ]; then
  echo "Error: Repository name and AWS region must be provided as arguments."
  exit 1
fi
REPO_NAME="$1"
AWS_REGION="$2"

# Function to check if an ECR repository exists
check_ecr_repo() {
  local repo=$1
  if aws ecr describe-repositories --repository-names "$repo" --region "$AWS_REGION" >/dev/null 2>&1; then
    return 0  # Repository exists
  else
    return 1  # Repository does not exist
  fi
}

# Delete ECR Repository
if check_ecr_repo "$REPO_NAME"; then
  echo "Deleting ECR repository: $REPO_NAME"
  aws ecr delete-repository --repository-name "$REPO_NAME" --force --region "$AWS_REGION" || { echo "Failed to delete $REPO_NAME"; exit 1; }
else
  echo "ECR repository $REPO_NAME does not exist, skipping deletion."
fi

echo "ECR repository cleanup completed successfully!"
