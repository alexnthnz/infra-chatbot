output "bedrock_role_arn" {
  description = "ARN of the Bedrock IAM role"
  value       = aws_iam_role.bedrock_kb_llm_kb.arn
}

output "bedrock_role_name" {
  description = "Name of the Bedrock IAM role"
  value       = aws_iam_role.bedrock_kb_llm_kb.name
}
