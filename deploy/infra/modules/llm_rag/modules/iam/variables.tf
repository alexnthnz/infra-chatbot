variable "kb_name" {
  description = "The knowledge base name."
  type        = string
  default     = "sample"
}

variable "s3_arn" {
  type = string
}

variable "kb_model_arn" {
  type = string
}
