variable "vpc_id" {
  description = "The ID of the VPC where the Lambda function will be deployed"
  type        = string
}

variable "secret_arn" {
  description = "The ARN of the secret in AWS Secrets Manager"
  type        = string
}

variable "lambda_function_name" {
  description = "The name of the Lambda function to be created"
  type        = string
}

variable "lambda_function_s3_bucket_arn" {
  description = "The ARN of the S3 bucket where the Lambda function code is stored"
  type        = string
}

variable "lambda_function_s3_bucket_name" {
  description = "The name of the S3 bucket where the Lambda function code is stored"
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

variable "lambda_function_subnet_ids" {
  description = "List of subnet IDs for the Lambda function"
  type        = list(string)
}

variable "lambda_security_group_id" {
  description = "Security group ID for the Lambda function"
  type        = string
}

variable "aurora_cluster_arn" {
  description = "The ARN of the Aurora cluster"
  type        = string
}

variable "file_s3_bucket_arn" {
  description = "The ARN of the S3 bucket where the file is stored"
  type        = string
}

variable "stage_name" {
  description = "The name of the stage for the API Gateway"
  type        = string
}
