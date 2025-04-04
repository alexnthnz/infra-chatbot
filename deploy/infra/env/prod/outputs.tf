output "agent_model_arn" {
  description = "ARN of the SageMaker agent model."
  value       = module.agent.agent_model_arn
}

output "agent_endpoint_config_name" {
  description = "Name of the SageMaker endpoint configuration for the agent model."
  value       = module.agent.agent_endpoint_config_name
}

output "agent_endpoint_name" {
  description = "Name of the SageMaker endpoint for the agent model."
  value       = module.agent.agent_endpoint_name
}

# Outputs for shared module
output "agent_model_role_arn" {
  description = "ARN of the IAM role for the agent model."
  value       = module.shared.agent_model_role_arn
}

output "foundation_model_role_arn" {
  description = "ARN of the IAM role for the foundation model."
  value       = module.shared.foundation_model_role_arn
}

output "s3_bucket_arn" {
  description = "ARN of the S3 bucket for model artifacts."
  value       = module.shared.s3_bucket_arn
}

output "agent_model_repo_url" {
  description = "The URL of the ECR repository for the agent model."
  value       = module.shared.agent_model_repo_url
}
