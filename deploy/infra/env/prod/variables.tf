variable "aws_region" {
  description = "AWS region for deployment"
  type        = string
  default     = "us-west-1"
}

variable "environment" {
  description = "The deployment environment identifier"
  type        = string
  default     = "prod"
}

variable "agent_model_role_name" {
  description = "IAM role name for the agent model in production"
  type        = string
  default     = "prod-agent-model-sagemaker-role"
}

variable "foundation_model_role_name" {
  description = "IAM role name for the foundation model in production"
  type        = string
  default     = "prod-foundation-model-sagemaker-role"
}

variable "model_artifacts_bucket_name" {
  description = "S3 bucket name for storing model artifacts in production"
  type        = string
  default     = "prod-model-artifacts-bucket"
}
