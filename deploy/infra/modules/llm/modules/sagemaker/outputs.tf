output "sagemaker_model_arn" {
  description = "ARN of the SageMaker agent model."
  value       = aws_sagemaker_model.llm.arn
}

output "sagemaker_endpoint_config_name" {
  description = "Name of the SageMaker endpoint configuration for the agent model."
  value       = aws_sagemaker_endpoint_configuration.llm_endpoint_configuration.name
}

output "sagemaker_endpoint_name" {
  description = "Name of the SageMaker endpoint for the agent model."
  value       = aws_sagemaker_endpoint.llm_endpoint.name
}
