output "sagemaker_model_arn" {
  description = "ARN of the SageMaker model."
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
