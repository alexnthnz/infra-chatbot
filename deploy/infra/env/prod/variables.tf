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
variable "elasticache_enabled" {
  description = "Flag to enable or disable ElastiCache."
  type        = bool
  default     = false
}

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

variable "lambda_function_ecr_image_uri" {
  description = "The ARN of the S3 bucket where the Lambda function code is stored."
  type        = string
}

##########################################
# SageMaker Variables
##########################################
variable "sagemaker_enabled" {
  description = "Flag to enable or disable SageMaker."
  type        = bool
  default     = false
}

variable "sagemaker_name" {
  description = "The name of the SageMaker model."
  type        = string
}

variable "sagemaker_ecr_image_uri" {
  description = "The URI of the SageMaker ECR image."
  type        = string
}

variable "sagemaker_initial_instance_count" {
  description = "The initial instance count for the SageMaker endpoint."
  type        = number
}

variable "sagemaker_instance_type" {
  description = "The instance type for the SageMaker endpoint."
  type        = string
}

variable "sagemaker_hf_model_id" {
  description = "The Hugging Face model ID."
  type        = string
}

variable "sagemaker_hf_access_token" {
  description = "The Hugging Face access token."
  type        = string
}

variable "sagemaker_tgi_config" {
  description = "The configuration for the SageMaker TGI."
  type = object({
    max_input_tokens       = number
    max_total_tokens       = number
    max_batch_total_tokens = number
  })
}
