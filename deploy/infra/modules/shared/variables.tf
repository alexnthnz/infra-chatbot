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
