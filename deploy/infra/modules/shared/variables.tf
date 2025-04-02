variable "agent_model_role_name" {
  description = "Name for the IAM role for the agent model."
  type        = string
}

variable "foundation_model_role_name" {
  description = "Name for the IAM role for the foundation model."
  type        = string
}

variable "model_artifacts_bucket_name" {
  description = "Name for the S3 bucket to store model artifacts."
  type        = string
}

# If you want to pass in the bucket ARN for IAM policy reference,
# you can either compute it from the S3 bucket resource (in s3.tf)
# or declare it as a variable.
