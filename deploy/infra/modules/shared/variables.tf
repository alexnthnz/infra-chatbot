variable "vpc_name" {
  description = "Name of the VPC."
  type        = string
}

variable "cidr_block" {
  description = "CIDR block for the VPC."
  type        = string
}

variable "aurora_name" {
  description = "Name of the Aurora database."
  type        = string
}

variable "aurora_master_username" {
  description = "Master username for the Aurora database."
  type        = string
}

variable "bastion_name" {
  description = "Name of the bastion host."
  type        = string
}

variable "ec2_bastion_ingress_ips" {
  description = "IP addresses for the bastion host ingress rule."
  type        = list(string)
}

variable "s3_bucket_handler_name" {
  description = "Name of the S3 bucket for file storage."
  type        = string
}

variable "elasticache_enabled" {
  description = "Enable ElastiCache."
  type        = bool
  default     = false
}

variable "elasticache_name" {
  description = "Name of the ElastiCache cluster."
  type        = string
}

variable "secret_name" {
  description = "Name of the secret in AWS Secrets Manager."
  type        = string
}
