variable "lambda_function_name" {
  description = "The name of the Lambda function to be created"
  type        = string
}

variable "aurora_cluster_arn" {
  description = "The ARN of the Aurora cluster"
  type        = string
}

variable "file_s3_bucket_arn" {
  description = "The ARN of the S3 bucket for file storage"
  type        = string
}

variable "secret_arn" {
  description = "The ARN of the secret in AWS Secrets Manager"
  type        = string
}
