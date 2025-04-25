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
