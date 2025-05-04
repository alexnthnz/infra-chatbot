variable "secret_name" {
  description = "The name of the secret to create"
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

variable "aurora_cluster_arn" {
  description = "The ARN of the Aurora cluster"
  type        = string
}

variable "file_s3_bucket_arn" {
  description = "The ARN of the S3 bucket where the file is stored"
  type        = string
}
