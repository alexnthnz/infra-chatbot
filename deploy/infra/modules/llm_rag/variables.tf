variable "aurora_cluster_endpoint" {
  description = "The endpoint of the Aurora cluster."
  type        = string
}

variable "aurora_cluster_port" {
  description = "The port of the Aurora cluster."
  type        = number
}

variable "aurora_cluster_master_username" {
  description = "The master username for the Aurora cluster."
  type        = string
}

variable "aurora_cluster_arn" {
  description = "The ARN of the Aurora cluster."
  type        = string
}

variable "aurora_cluster_resource_id" {
  description = "The resource ID of the Aurora cluster."
  type        = string
}

variable "aurora_secret_arn" {
  description = "The ARN of the Aurora secret."
  type        = string
}

variable "kb_s3_bucket_name_prefix" {
  description = "The name prefix of the S3 bucket for the data source of the knowledge base."
  type        = string
}

variable "kb_model_id" {
  description = "The ID of the foundational model used by the knowledge base."
  type        = string
}

variable "kb_name" {
  description = "The name of the knowledge base."
  type        = string
}

variable "sagemaker_name" {
  description = "The name of the SageMaker instance."
  type        = string
}

variable "sagemaker_instance_type" {
  description = "The instance type for the SageMaker model."
  type        = string
}

variable "sagemaker_initial_instance_count" {
  description = "The initial instance count for the SageMaker model."
  type        = number
}

variable "sagemaker_ecr_image_uri" {
  description = "The ECR image URI for the SageMaker model."
  type        = string
}
