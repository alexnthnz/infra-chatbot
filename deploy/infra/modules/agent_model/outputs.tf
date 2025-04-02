output "agent_model_arn" {
  description = "ARN of the SageMaker agent model."
  value       = aws_sagemaker_model.agent_model.arn
}

output "agent_endpoint_config_name" {
  description = "Name of the SageMaker endpoint configuration for the agent model."
  value       = aws_sagemaker_endpoint_configuration.agent_endpoint_config.name
}

output "agent_endpoint_name" {
  description = "Name of the SageMaker endpoint for the agent model."
  value       = aws_sagemaker_endpoint.agent_endpoint.name
}
