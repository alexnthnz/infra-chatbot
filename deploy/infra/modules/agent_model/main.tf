resource "aws_sagemaker_model" "agent_model" {
  name               = var.model_name
  execution_role_arn = var.execution_role_arn

  primary_container {
    image             = var.ecr_image_uri
  }
}

resource "aws_sagemaker_endpoint_configuration" "agent_endpoint_config" {
  name = "${var.model_name}-config"

  production_variants {
    variant_name          = "default"
    model_name            = aws_sagemaker_model.agent_model.name
    initial_instance_count = var.initial_instance_count
    instance_type         = var.instance_type
  }
}

resource "aws_sagemaker_endpoint" "agent_endpoint" {
  name                = "${var.model_name}-endpoint"
  endpoint_config_name = aws_sagemaker_endpoint_configuration.agent_endpoint_config.name
}
