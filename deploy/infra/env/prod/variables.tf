variable "aws_region" {
  description = "The AWS region to deploy the resources."
  type        = string
}

#############################################
# VPC Variables
#############################################

variable "vpc_name" {
  description = "Name of the VPC."
  type        = string
}

variable "cidr_block" {
  description = "CIDR block for the VPC."
  type        = string
}

###############################################
# Aurora Variables
###############################################

variable "aurora_name" {
  description = "The name of the Aurora database."
  type        = string
}

variable "aurora_master_username" {
  description = "The master username for the Aurora database."
  type        = string
}

################################################
# Bastion Variables
################################################

variable "bastion_name" {
  description = "The name of the bastion host."
  type        = string
}

variable "ec2_bastion_ingress_ips" {
  description = "IP addresses for the bastion host ingress rule."
  type        = list(string)
}

#########################################
# Knowledge Base Variables
#########################################
variable "kb_name" {
  description = "The name of the knowledge base."
  type        = string
}

variable "kb_s3_bucket_name_prefix" {
  description = "The name prefix of the S3 bucket for the data source of the knowledge base."
  type        = string
}

variable "kb_oss_collection_name" {
  description = "The name of the OpenSearch Service (OSS) collection for the knowledge base."
  type        = string
}

variable "kb_model_id" {
  description = "The ID of the foundational model used by the knowledge base."
  type        = string
}

##########################################
# Lambda Handler Variables
##########################################

