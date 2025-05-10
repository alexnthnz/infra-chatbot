output "arn" {
  description = "The ARN of the ECR repository"
  value       = aws_ecr_repository.repository.arn
}

output "registry_id" {
  description = "The AWS account ID associated with the ECR registry"
  value       = aws_ecr_repository.repository.registry_id
}

output "repository_url" {
  description = "The URL of the ECR repository"
  value       = aws_ecr_repository.repository.repository_url
}
