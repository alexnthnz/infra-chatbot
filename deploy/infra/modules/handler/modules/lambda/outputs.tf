output "lambda_function_arn" {
  description = "ARN of the Lambda function"
  value       = aws_lambda_function.app.arn
}

output "lambda_function_invoke_arn" {
  description = "Invoke ARN of the Lambda function"
  value       = aws_lambda_function.app.invoke_arn
}

output "lambda_function_name" {
  description = "Name of the Lambda function"
  value       = aws_lambda_function.app.function_name
}
