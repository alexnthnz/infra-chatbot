terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.48"
    }
    opensearch = {
      source  = "opensearch-project/opensearch"
      version = "~> 2.3.0"
    }
    awscc = {
      source  = "hashicorp/awscc"
      version = "~> 1.0"
    }
  }

  backend "s3" {
    bucket         = "infra-chatbot-remote-state"
    key            = "app/terraform.tfstate"
    dynamodb_table = "infra-chatbot-remote-state"
    region         = "ap-southeast-2"
    encrypt        = true
  }
}

provider "aws" {
  region = var.aws_region
}

