variable "lambda_function_ecr_image_uri" {
  description = "The ECR image URI for the Lambda function"
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
