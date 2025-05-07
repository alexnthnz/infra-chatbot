variable "vpc_id" {
  description = "VPC ID"
  type        = string
}

variable "aurora_security_group_id" {
  description = "Aurora Security Group ID"
  type        = string
}

variable "elasticache_security_group_id" {
  description = "ElastiCache Security Group ID"
  type        = string
}
