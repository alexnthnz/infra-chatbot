variable "kb_name" {
  type        = string
  description = "The name of the Knowledge Base"
}

variable "s3_arn" {
  type        = string
  description = "The ARN of the S3 bucket"
}

variable "bedrock_role_arn" {
  type        = string
  description = "The ARN of the Bedrock role"
}

variable "bedrock_role_name" {
  type        = string
  description = "The name of the Bedrock role"
}

variable "kb_model_arn" {
  type        = string
  description = "The ARN of the Knowledge Base model"
}

variable "aurora_cluster_arn" {
  type        = string
  description = "The ARN of the OpenSearch domain"
}

variable "aurora_cluster_resource_id" {
  type        = string
  description = "The resource ID of the OpenSearch domain"
}

variable "aurora_secret_arn" {
  type        = string
  description = "The ARN of the OpenSearch secret"
}
