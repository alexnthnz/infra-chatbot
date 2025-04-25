output "sagemaker_model_arn" {
  description = "ARN of the SageMaker agent model."
  value       = aws_sagemaker_model.sagemaker_model_llm_model.arn
}

output "sagemaker_endpoint_config_name" {
  description = "Name of the SageMaker endpoint configuration for the agent model."
  value       = aws_sagemaker_endpoint_configuration.sagemaker_endpoint_config_llm_model.name
}

output "sagemaker_endpoint_name" {
  description = "Name of the SageMaker endpoint for the agent model."
  value       = aws_sagemaker_endpoint.sagemaker_endpoint_llm_model.name
}
