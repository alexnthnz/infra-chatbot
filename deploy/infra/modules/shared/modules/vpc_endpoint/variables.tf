variable "vpc_id" {
  description = "VPC ID"
  type        = string
}

variable "vpc_subnet_ids" {
  description = "Subnet IDs"
  type        = list(string)
}

variable "security_group_ids" {
  description = "Security Group IDs"
  type        = list(string)
}
