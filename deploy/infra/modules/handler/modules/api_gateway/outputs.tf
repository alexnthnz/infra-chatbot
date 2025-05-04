output "api_invoke_url" {
  description = "Invoke URL of the API Gateway"
  value       = "${aws_api_gateway_deployment.deployment.invoke_url}/${var.stage}"
}
