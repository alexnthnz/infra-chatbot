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

variable "aws_region" {
  description = "AWS region where the resources will be created."
  type        = string
}

variable "project" {
  description = "Project name for tagging resources."
  type        = string
}

variable "environment" {
  description = "Deployment environment identifier."
  type        = string
  default     = "dev"
}

variable "cidr_block" {
  description = "CIDR block for the VPC."
  type        = string
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
# If you want to pass in the bucket ARN for IAM policy reference,
# you can either compute it from the S3 bucket resource (in s3.tf)
# or declare it as a variable.
