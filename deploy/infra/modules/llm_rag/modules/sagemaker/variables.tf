variable "sagemaker_name" {
  description = "Name of the SageMaker model and endpoint"
  type        = string
}

variable "sagemaker_role_arn" {
  description = "ARN of the SageMaker execution role"
  type        = string
}

variable "sagemaker_instance_type" {
  description = "SageMaker instance type for the model"
  type        = string
}

variable "sagemaker_initial_instance_count" {
  description = "Initial instance count for the SageMaker model"
  type        = number
}

variable "sagemaker_ecr_image_uri" {
  description = "ECR image URI for the SageMaker model"
  type        = string
}
