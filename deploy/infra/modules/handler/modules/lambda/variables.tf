variable "lambda_s3_bucket_name" {
  description = "The name of the S3 bucket to store artifacts"
  type        = string
}

variable "lambda_zip_key" {
  description = "The S3 key for the Lambda zip file"
  type        = string
}

variable "lambda_layer_zip_key" {
  description = "The S3 key for the Lambda layer zip file"
  type        = string
}

variable "lambda_function_name" {
  description = "The name of the Lambda function"
  type        = string
}

variable "lambda_role_arn" {
  description = "The ARN of the IAM role for the Lambda function"
  type        = string
}

variable "lambda_security_group_id" {
  description = "The security group ID for the Lambda function"
  type        = string
}

variable "secret_arn" {
  description = "The ARN of the secret in AWS Secrets Manager"
  type        = string
}

variable "vpc_id" {
  description = "The ID of the VPC where the Lambda function will be deployed"
  type        = string
}

variable "subnet_ids" {
  description = "List of subnet IDs for the Lambda function"
  type        = list(string)
}
