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

#########################################
# Knowledge Base Variables
#########################################
variable "kb_name" {
  description = "The name of the knowledge base."
  type        = string
}

variable "kb_s3_bucket_name_prefix" {
  description = "The name prefix of the S3 bucket for the data source of the knowledge base."
  type        = string
}

variable "kb_oss_collection_name" {
  description = "The name of the OpenSearch Service (OSS) collection for the knowledge base."
  type        = string
}

variable "kb_model_id" {
  description = "The ID of the foundational model used by the knowledge base."
  type        = string
}

variable "sagemaker_name" {
  description = "The name of the SageMaker instance."
  type        = string
}

variable "sagemaker_instance_type" {
  description = "The instance type for the SageMaker model."
  type        = string
  default     = "ml.t2.medium"
}

variable "sagemaker_initial_instance_count" {
  description = "The initial instance count for the SageMaker model."
  type        = number
  default     = 1
}

variable "sagemaker_ecr_image_uri" {
  description = "The ECR image URI for the SageMaker model."
  type        = string
}
