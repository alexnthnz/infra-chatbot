variable "ec2_bastion_ingress_ips" {
  description = "IPs address for the bastion host ingress rule"
  type        = list(string)
}

variable "vpc_id" {
  description = "VPC ID"
  type        = string
}

variable "bastion_name" {
  description = "Name of the bastion host"
  type        = string
}

variable "public_subnet_id" {
  description = "Public subnet ID for the bastion host"
  type        = string
}

variable "aurora_security_group_id" {
  description = "Security group ID for the Aurora cluster"
  type        = string
}

variable "key_pair_path" {
  description = "Path to store the key pair files"
  type        = string
  default     = "./keys"
}
