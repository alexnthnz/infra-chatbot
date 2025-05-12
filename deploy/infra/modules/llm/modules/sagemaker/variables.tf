variable "sagemaker_name" {
  description = "The name of the SageMaker model."
  type        = string
}

variable "sagemaker_execution_role_arn" {
  description = "The ARN of the SageMaker execution role."
  type        = string
}

variable "sagemaker_ecr_image_uri" {
  description = "The URI of the SageMaker ECR image."
  type        = string
}

variable "sagemaker_initial_instance_count" {
  description = "The initial instance count for the SageMaker endpoint."
  type        = number
}

variable "sagemaker_instance_type" {
  description = "The instance type for the SageMaker endpoint."
  type        = string
}

variable "sagemaker_hf_model_id" {
  description = "The Hugging Face model ID."
  type        = string
}

variable "sagemaker_hf_access_token" {
  description = "The Hugging Face access token."
  type        = string
}

variable "sagemaker_tgi_config" {
  description = "The configuration for the SageMaker TGI."
  type = object({
    max_input_tokens       = number
    max_total_tokens       = number
    max_batch_total_tokens = number
  })
}
