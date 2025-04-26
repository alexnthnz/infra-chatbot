resource "aws_sagemaker_model" "sagemaker_model_llm_model" {
  name               = "${var.sagemaker_name}-${formatdate("YYYYMMDDHHmmss", timestamp())}"
  execution_role_arn = var.sagemaker_role_arn

  primary_container {
    image = var.sagemaker_ecr_image_uri
  }
}

resource "aws_sagemaker_endpoint_configuration" "sagemaker_endpoint_config_llm_model" {
  name = "${var.sagemaker_name}-config-${formatdate("YYYYMMDDHHmmss", timestamp())}"

  production_variants {
    variant_name           = "default"
    model_name             = aws_sagemaker_model.sagemaker_model_llm_model.name
    initial_instance_count = var.sagemaker_initial_instance_count
    instance_type          = var.sagemaker_instance_type
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_sagemaker_endpoint" "sagemaker_endpoint_llm_model" {
  name                 = "${var.sagemaker_name}-endpoint"
  endpoint_config_name = aws_sagemaker_endpoint_configuration.sagemaker_endpoint_config_llm_model.name
}
