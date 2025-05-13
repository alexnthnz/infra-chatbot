###############################################################################
# Outputs for the shared module
###############################################################################
output "vpc_id" {
  description = "The ID of the VPC"
  value       = module.shared.vpc_id
}

output "vpc_arn" {
  description = "The ARN of the VPC"
  value       = module.shared.vpc_arn
}

output "vpc_cidr" {
  description = "The CIDR block of the VPC"
  value       = module.shared.vpc_cidr_block
}

output "aurora_cluster_arn" {
  description = "Amazon Resource Name (ARN) of cluster"
  value       = module.shared.aurora_cluster_arn
}

output "aurora_cluster_id" {
  description = "The RDS Cluster Identifier"
  value       = module.shared.aurora_cluster_id
}

output "aurora_cluster_resource_id" {
  description = "The RDS Cluster Resource ID"
  value       = module.shared.aurora_cluster_resource_id
}

output "aurora_cluster_members" {
  description = "List of RDS Instances that are a part of this cluster"
  value       = module.shared.aurora_cluster_members
}

output "aurora_cluster_endpoint" {
  description = "Writer endpoint for the cluster"
  value       = module.shared.aurora_cluster_endpoint
}

output "aurora_cluster_reader_endpoint" {
  description = "A read-only endpoint for the cluster, automatically load-balanced across replicas"
  value       = module.shared.aurora_cluster_reader_endpoint
}

output "aurora_cluster_engine_version_actual" {
  description = "The running version of the cluster database"
  value       = module.shared.aurora_cluster_engine_version_actual
}

# database_name is not set on `aws_rds_cluster` resource if it was not specified, so can't be used in output
output "aurora_cluster_database_name" {
  description = "Name for an automatically created database on cluster creation"
  value       = module.shared.aurora_cluster_database_name
}

output "aurora_cluster_port" {
  description = "The database port"
  value       = module.shared.aurora_cluster_port
}

output "aurora_cluster_master_user_secret" {
  description = "The secret ARN for the master user"
  value       = module.shared.aurora_cluster_master_user_secret
}


output "bastion_instance_id" {
  description = "The ID of the bastion instance"
  value       = module.shared.bastion_instance_id
}

output "bastion_public_ip" {
  description = "The public IP address of the bastion host"
  value       = module.shared.bastion_public_ip
}

output "bastion_security_group_id" {
  description = "The ID of the security group attached to the bastion host"
  value       = module.shared.bastion_security_group_id
}

output "bastion_private_key_path" {
  description = "The path to the private key file for SSH access"
  value       = module.shared.bastion_private_key_path
  sensitive   = true
}

output "bastion_public_key_path" {
  description = "The path to the public key file for reference"
  value       = module.shared.bastion_public_key_path
}

output "file_bucket_name" {
  description = "The name of the S3 bucket created"
  value       = module.shared.file_s3_bucket_name
}

output "file_bucket_arn" {
  description = "The ARN of the S3 bucket created"
  value       = module.shared.file_s3_bucket_arn
}

output "elasticache_arn" {
  description = "The ARN of the ElastiCache cluster"
  value       = module.shared.elasticache_arn
}

output "elasticache_endpoint" {
  description = "The endpoint of the ElastiCache cluster"
  value       = module.shared.elasticache_endpoint
}

#############################################################################
# Outputs for the rag module
#############################################################################
output "rag_s3_arn" {
  description = "arn of the S3 bucket created"
  value       = module.rag.s3_arn
}

output "rag_s3_bucket_name" {
  description = "Name of the S3 bucket created"
  value       = module.rag.s3_bucket_name
}

output "rag_knowledge_base_id" {
  description = "The ID of the Bedrock Agent Knowledge Base"
  value       = module.rag.knowledge_base_id
}

output "rag_knowledge_base_arn" {
  description = "The ARN of the Bedrock Agent Knowledge Base"
  value       = module.rag.knowledge_base_arn
}

#############################################################################
# Outputs for the llm module
#############################################################################
output "sagemaker_model_arn" {
  description = "ARN of the SageMaker model."
  value       = var.sagemaker_enabled ? module.llm.sagemaker_model_arn : null
}

output "sagemaker_endpoint_config_name" {
  description = "Name of the SageMaker endpoint configuration for the agent model."
  value       = var.sagemaker_enabled ? module.llm.sagemaker_endpoint_config_name : null
}

output "sagemaker_endpoint_name" {
  description = "Name of the SageMaker endpoint for the agent model."
  value       = var.sagemaker_enabled ? module.llm.sagemaker_endpoint_name : null
}
