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

variable "aurora_cluster_id" {
  type        = string
  description = "The ID of the Aurora RDS domain"
}

variable "aurora_cluster_arn" {
  type        = string
  description = "The ARN of the Aurora RDS domain"
}

variable "aurora_cluster_resource_id" {
  type        = string
  description = "The resource ID of the Aurora RDS domain"
}

variable "aurora_secret_arn" {
  type        = string
  description = "The ARN of the Aurora RDS secret"
}

variable "aurora_cluster_endpoint" {
  type        = string
  description = "The endpoint of the Aurora RDS domain"
}

variable "aurora_cluster_port" {
  type        = number
  description = "The port of the Aurora RDS domain"
}

variable "aurora_cluster_master_username" {
  type        = string
  description = "The master username for the Aurora RDS domain"
}

variable "bastion_private_key_path" {
  type        = string
  description = "The path to the private key for the bastion host"
}

variable "bastion_public_ip" {
  type        = string
  description = "The public IP address of the bastion host"
}
