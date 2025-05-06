variable "kb_name" {
  description = "The knowledge base name."
  type        = string
}

variable "aurora_cluster_arn" {
  description = "The RDS Cluster ARN"
  type        = string
}

variable "aurora_secret_arn" {
  description = "The RDS Secret ARN"
  type        = string
}

variable "s3_arn" {
  type = string
}

variable "kb_model_arn" {
  type = string
}
