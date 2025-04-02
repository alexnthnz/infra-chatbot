terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0" # Use a stable, recent version
    }
  }

  backend s3 {
    bucket         = "infra-chatbot-remote-state" 
    key            = "app/terraform.tfstate"
    dynamodb_table = "infra-chatbot-remote-state"
    region         = "ap-southeast-2"
    encrypt        = true
  }
}

provider "aws" {
  profile                  = "default"
  shared_credentials_files = ["~/.aws/credentials"]
  region = var.aws_region
}

