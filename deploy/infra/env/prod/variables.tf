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

###################################################
# ElastiCache Variables
###################################################
variable "elasticache_name" {
  description = "The name of the ElastiCache cluster."
  type        = string
}

##############################################
# Secrets Manager Variables
##############################################
variable "secret_name" {
  description = "The name of the secret in AWS Secrets Manager."
  type        = string
}

###############################################
# S3 Bucket Variables
###############################################
variable "s3_bucket_handler_name" {
  description = "The name of the S3 bucket for file storage."
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
variable "lambda_function_handler_name" {
  description = "The name of the Lambda function to be created."
  type        = string
}

variable "lambda_function_handler_s3_bucket_arn" {
  description = "The ARN of the S3 bucket where the Lambda function code is stored."
  type        = string
}

variable "lambda_function_handler_s3_bucket_name" {
  description = "The name of the S3 bucket where the Lambda function code is stored."
  type        = string
}

variable "lambda_function_handler_zip_key" {
  description = "The S3 key for the Lambda function code."
  type        = string
}
