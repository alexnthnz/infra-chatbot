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
    echo "ECR repository $repo already exists."
    return 0  # Repository exists
  else
    echo "ECR repository $repo does not exist."
    return 1  # Repository does not exist
  fi
}

# Create ECR Repository
if ! check_ecr_repo "$REPO_NAME"; then
  echo "Creating ECR repository: $REPO_NAME"
  aws ecr create-repository --repository-name "$REPO_NAME" --region "$AWS_REGION" || { echo "Failed to create $REPO_NAME"; exit 1; }
else
  echo "Skipping creation of $REPO_NAME as it already exists."
fi

# Output the repository name for reference
echo "ECR repository: $REPO_NAME"
