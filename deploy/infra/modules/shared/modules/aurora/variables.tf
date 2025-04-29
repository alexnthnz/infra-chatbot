variable "aurora_name" {
  description = "The name of the Aurora cluster"
  type        = string
}

variable "aurora_master_username" {
  description = "The master username for the Aurora cluster"
  type        = string
}

variable "aurora_master_password" {
  description = "The master password for the Aurora cluster"
  type        = string
}

variable "vpc_id" {
  description = "The ID of the VPC"
  type        = string
}

variable "database_subnet_ids" {
  description = "The subnet IDs for the VPC"
  type        = list(string)
}
