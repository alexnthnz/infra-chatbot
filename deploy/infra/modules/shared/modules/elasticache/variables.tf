variable "elasticache_name" {
  description = "The name of the ElastiCache cluster"
  type        = string
}

variable "vpc_id" {
  description = "The ID of the VPC where the ElastiCache cluster will be created"
  type        = string
}

variable "vpc_cidr_block" {
  description = "The CIDR block of the VPC"
  type        = string
}

variable "vpc_subnet_ids" {
  description = "The list of subnet IDs where the ElastiCache cluster will be created"
  type        = list(string)
}
