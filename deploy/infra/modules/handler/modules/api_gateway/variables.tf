variable "api_gateway_name" {
  description = "The name of the API Gateway"
  type        = string
}

variable "lambda_invoke_arn" {
  description = "The ARN of the Lambda function to be invoked"
  type        = string
}

variable "lambda_function_name" {
  description = "The name of the Lambda function to be invoked"
  type        = string
}

variable "stage_name" {
  description = "The name of the stage for the API Gateway"
  type        = string
}
