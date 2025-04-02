variable "model_name" {
  description = "Name for the SageMaker agent model."
  type        = string
}

variable "execution_role_arn" {
  description = "IAM role ARN for SageMaker to assume for the agent model."
  type        = string
}

variable "image_uri" {
  description = "Container image URI for the agent model."
  type        = string
}

variable "model_data_url" {
  description = "S3 URL for the model artifacts."
  type        = string
}

variable "instance_type" {
  description = "SageMaker instance type for the endpoint."
  type        = string
  default     = "ml.t2.medium"
}

# Optionally, pass additional variables as needed (e.g., initial instance count)
variable "initial_instance_count" {
  description = "Initial instance count for the endpoint."
  type        = number
  default     = 1
}
