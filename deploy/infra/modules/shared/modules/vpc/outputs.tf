output "vpc_id" {
  description = "The ID of the VPC."
  value       = module.vpc.vpc_id
}

output "vpc_arn" {
  description = "The ARN of the VPC."
  value       = module.vpc.vpc_arn
}

output "vpc_cidr_block" {
  description = "The CIDR block of the VPC."
  value       = module.vpc.vpc_cidr_block
}

output "vpc_database_subnet_group_name" {
  description = "The name of the database subnet group."
  value       = module.vpc.database_subnet_group_name
}

output "vpc_private_subnets_cidr_blocks" {
  description = "The CIDR blocks of the private subnets."
  value       = module.vpc.private_subnets_cidr_blocks
}

output "vpc_private_subnets" {
  description = "The IDs of the private subnets."
  value       = module.vpc.private_subnets
}

output "vpc_public_subnets_cidr_blocks" {
  description = "The CIDR blocks of the public subnets."
  value       = module.vpc.public_subnets_cidr_blocks
}

output "vpc_public_subnets" {
  description = "The IDs of the public subnets."
  value       = module.vpc.public_subnets
}

output "vpc_database_subnets_cidr_blocks" {
  description = "The CIDR blocks of the database subnets."
  value       = module.vpc.database_subnets_cidr_blocks
}

output "vpc_database_subnets" {
  description = "The IDs of the database subnets."
  value       = module.vpc.database_subnets
}

output "vpc_intra_subnets_cidr_blocks" {
  description = "The CIDR blocks of the intra subnets."
  value       = module.vpc.intra_subnets_cidr_blocks
}

output "vpc_intra_subnets" {
  description = "The IDs of the intra subnets."
  value       = module.vpc.intra_subnets
}
