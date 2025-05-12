output "sagemaker_role_arn" {
  value = aws_iam_role.llm_exec.arn
}
