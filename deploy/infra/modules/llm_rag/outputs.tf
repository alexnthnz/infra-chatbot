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

output "opensearch_collection_arn" {
  description = "The name of the collection for the Knowledge Base Open Source Software (OSS) content"
  value       = module.opensearch.opensearch_collection_arn
}

output "opensearch_index_name" {
  description = "The name of the OpenSearch index"
  value       = module.opensearch.opensearch_index_name
}

output "knowledge_base_id" {
  description = "The ID of the Bedrock Agent Knowledge Base"
  value       = module.knowledge_base.knowledge_base_id
}

output "knowledge_base_arn" {
  description = "The ARN of the Bedrock Agent Knowledge Base"
  value       = module.knowledge_base.knowledge_base_arn
}

output "sagemaker_model_arn" {
  description = "ARN of the SageMaker agent model."
  value       = module.sagemaker.sagemaker_model_arn
}

output "sagemaker_endpoint_config_name" {
  description = "Name of the SageMaker endpoint configuration for the agent model."
  value       = module.sagemaker.sagemaker_endpoint_config_name
}

output "sagemaker_endpoint_name" {
  description = "Name of the SageMaker endpoint for the agent model."
  value       = module.sagemaker.sagemaker_endpoint_name
}
