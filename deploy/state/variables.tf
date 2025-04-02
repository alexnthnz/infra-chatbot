variable "aws_s3_bucket" {
  type        = string
  description = "The name of the S3 bucket that will be used for the Terraform state."
  default     = "terraform-state"
}

variable "aws_region" {
  type        = string
  description = "The AWS region that will be used for the resources."
  default     = "ap-southeast-2"
}

variable "aws_dynamodb_table" {
  type        = string
  description = "The name of the DynamoDB table that will be used for the Terraform state."
  default     = "terraform-state"
}
