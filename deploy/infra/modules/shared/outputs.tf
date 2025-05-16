##################################################################
# Outputs for the VPC and Aurora cluster modules
##################################################################
output "vpc_id" {
  description = "The ID of the VPC"
  value       = module.vpc.vpc_id
}

output "vpc_arn" {
  description = "The ARN of the VPC"
  value       = module.vpc.vpc_arn
}

output "vpc_cidr_block" {
  description = "The CIDR block of the VPC"
  value       = module.vpc.vpc_cidr_block
}

output "vpc_public_subnet_ids" {
  description = "The IDs of the public subnets in the VPC"
  value       = module.vpc.vpc_public_subnets
}

output "vpc_private_subnet_ids" {
  description = "The IDs of the private subnets in the VPC"
  value       = module.vpc.vpc_private_subnets
}

output "vpc_database_subnet_ids" {
  description = "The IDs of the database subnets in the VPC"
  value       = module.vpc.vpc_database_subnets
}

output "vpc_intra_subnet_ids" {
  description = "The IDs of the intra subnets in the VPC"
  value       = module.vpc.vpc_intra_subnets
}

##############################################
# Outputs for the Aurora cluster module
##############################################

output "aurora_cluster_arn" {
  description = "Amazon Resource Name (ARN) of cluster"
  value       = module.aurora.cluster_arn
}

output "aurora_cluster_id" {
  description = "The RDS Cluster Identifier"
  value       = module.aurora.cluster_id
}

output "aurora_cluster_resource_id" {
  description = "The RDS Cluster Resource ID"
  value       = module.aurora.cluster_resource_id
}

output "aurora_cluster_members" {
  description = "List of RDS Instances that are a part of this cluster"
  value       = module.aurora.cluster_members
}

output "aurora_cluster_endpoint" {
  description = "Writer endpoint for the cluster"
  value       = module.aurora.cluster_endpoint
}

output "aurora_cluster_reader_endpoint" {
  description = "A read-only endpoint for the cluster, automatically load-balanced across replicas"
  value       = module.aurora.cluster_reader_endpoint
}

output "aurora_cluster_engine_version_actual" {
  description = "The running version of the cluster database"
  value       = module.aurora.cluster_engine_version_actual
}

# database_name is not set on `aws_rds_cluster` resource if it was not specified, so can't be used in output
output "aurora_cluster_database_name" {
  description = "Name for an automatically created database on cluster creation"
  value       = module.aurora.cluster_database_name
}

output "aurora_cluster_port" {
  description = "The database port"
  value       = module.aurora.cluster_port
}

output "aurora_cluster_master_user_secret" {
  description = "The secret ARN for the master user"
  value       = module.aurora.cluster_master_user_secret
}

output "aurora_cluster_master_username" {
  description = "The master username for the cluster"
  value       = module.aurora.cluster_master_username
}

output "aurora_cluster_security_group_id" {
  description = "The security group ID of the Aurora cluster"
  value       = module.aurora.cluster_security_group_id
}

################################################
# Outputs for the Bastion host module
################################################
output "bastion_instance_id" {
  description = "The ID of the bastion instance"
  value       = module.bastion.bastion_instance_id
}

output "bastion_public_ip" {
  description = "The public IP address of the bastion host"
  value       = module.bastion.bastion_public_ip
}

output "bastion_security_group_id" {
  description = "The ID of the security group attached to the bastion host"
  value       = module.bastion.bastion_security_group_id
}

output "bastion_private_key_path" {
  description = "The path to the private key file for SSH access"
  value       = module.bastion.private_key_path
}

output "bastion_public_key_path" {
  description = "The path to the public key file for reference"
  value       = module.bastion.public_key_path
}

#############################################
# Outputs for the S3 bucket module
#############################################
output "file_s3_bucket_name" {
  description = "The name of the S3 bucket"
  value       = module.file_bucket.s3_bucket_name
}

output "file_s3_bucket_arn" {
  description = "The ARN of the S3 bucket"
  value       = module.file_bucket.s3_bucket_arn
}

##############################################
# Outputs for the ElastiCache module
##############################################
output "elasticache_arn" {
  description = "The ARN of the ElastiCache cluster"
  value       = var.elasticache_enabled ? module.elasticache[0].elasticache_arn : null
}

output "elasticache_endpoint" {
  description = "The endpoint of the ElastiCache cluster"
  value       = var.elasticache_enabled ? module.elasticache[0].elasticache_endpoint : null
}

output "elasticache_security_group_id" {
  description = "The security group ID of the ElastiCache cluster"
  value       = var.elasticache_enabled ? module.elasticache[0].elasticache_security_group_id : null
}

##############################################
# Outputs for the Secrets Manager module
##############################################
output "secret_arn" {
  description = "ARN of the Secrets Manager secret"
  value       = module.secrets_manager.secret_arn
}

###################################################
# Outputs for the Security Group module
###################################################
output "lambda_security_group_id" {
  description = "The ID of the security group"
  value       = module.security_group.lambda_security_group_id
}
