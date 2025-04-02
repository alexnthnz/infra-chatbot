output "agent_model_role_arn" {
  description = "ARN of the IAM role for the agent model."
  value       = aws_iam_role.agent_model_role.arn
}

output "foundation_model_role_arn" {
  description = "ARN of the IAM role for the foundation model."
  value       = aws_iam_role.foundation_model_role.arn
}

output "s3_bucket_arn" {
  description = "ARN of the S3 bucket for model artifacts."
  value       = aws_s3_bucket.model_artifacts.arn
}

output "agent_model_repo_url" {
  description = "The URL of the ECR repository for the agent model."
  value       = aws_ecr_repository.agent_model_repo.repository_url
}
