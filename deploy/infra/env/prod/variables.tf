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

variable "project" {
  description = "Project name for tagging resources"
  type        = string
}

variable "cidr_block" {
  type        = string
  description = "The CIDR block that will be used for the VPC."
}

variable "rds_postgres_db_name" {
  description = "Name of the PostgreSQL database."
  type        = string
}

variable "rds_postgres_username" {
  description = "Username for the PostgreSQL database."
  type        = string
}

variable "rds_postgres_password" {
  description = "Password for the PostgreSQL database."
  type        = string
  sensitive   = true
}

variable "rds_postgres_instance_type" {
  description = "Instance type for the PostgreSQL database."
  type        = string
}

variable "rds_postgres_port" {
  description = "Port for the PostgreSQL database."
  type        = number
  default     = 5432
}

variable "elasticache_redis_port" {
  description = "Port for the ElastiCache Redis cluster."
  type        = number
  default     = 6379
}

variable "elasticache_redis_instance_type" {
  description = "Instance type for the ElastiCache Redis cluster."
  type        = string
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

variable "agent_model_name" {
  description = "Name for the SageMaker agent model."
  type        = string
  default     = "prod-agent-model"
}

variable "agent_ecr_image_uri" {
  description = "Container image URI for the agent model."
  type        = string
  default     = "prod-agent-model-ecr-image-uri"
}

variable "agent_instance_type" {
  description = "SageMaker instance type for the agent model."
  type        = string
  default     = "ml.t2.medium"
}

variable "agent_initial_instance_count" {
  description = "Initial instance count for the agent model."
  type        = number
  default     = 1
}
