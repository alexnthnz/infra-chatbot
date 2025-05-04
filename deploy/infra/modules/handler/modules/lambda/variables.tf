variable "lambda_artifacts_bucket_name" {
  description = "The name of the S3 bucket to store artifacts"
  type        = string
}

variable "lambda_zip_key" {
  description = "The S3 key for the Lambda zip file"
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

variable "secret_arn" {
  description = "The ARN of the secret in AWS Secrets Manager"
  type        = string
}

variable "subnet_ids" {
  description = "List of subnet IDs for the Lambda function"
  type        = list(string)
}

variable "security_group_ids" {
  description = "List of security group IDs for the Lambda function"
  type        = list(string)
}
