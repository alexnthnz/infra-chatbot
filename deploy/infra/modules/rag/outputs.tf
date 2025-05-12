output "s3_arn" {
  description = "arn of the S3 bucket created"
  value       = module.s3_bucket.arn
}

output "s3_bucket_name" {
  description = "Name of the S3 bucket created"
  value       = module.s3_bucket.bucket_name
}

output "bedrock_role_arn" {
  description = "ARN of the Bedrock IAM role"
  value       = module.iam.bedrock_role_arn
}

output "bedrock_role_name" {
  description = "Name of the Bedrock IAM role"
  value       = module.iam.bedrock_role_name
}

output "knowledge_base_id" {
  description = "The ID of the Bedrock Agent Knowledge Base"
  value       = module.knowledge_base.knowledge_base_id
}

output "knowledge_base_arn" {
  description = "The ARN of the Bedrock Agent Knowledge Base"
  value       = module.knowledge_base.knowledge_base_arn
}
