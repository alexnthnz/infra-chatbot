resource "aws_sagemaker_model" "llm" {
  name               = "${var.sagemaker_name}-${formatdate("YYYYMMDDHHmmss", timestamp())}"
  execution_role_arn = var.sagemaker_execution_role_arn

  primary_container {
    image = var.sagemaker_ecr_image_uri
    environment = {
      HF_MODEL_ID            = var.sagemaker_hf_model_id
      HF_TOKEN               = var.sagemaker_hf_access_token
      SM_NUM_GPUS            = local.num_gpus
      MAX_INPUT_LENGTH       = var.sagemaker_tgi_config.max_input_tokens
      MAX_TOTAL_TOKENS       = var.sagemaker_tgi_config.max_total_tokens
      MAX_BATCH_TOTAL_TOKENS = var.sagemaker_tgi_config.max_batch_total_tokens
      MESSAGES_API_ENABLED   = "true"
    }
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_sagemaker_endpoint_configuration" "llm_endpoint_configuration" {
  name = "${var.sagemaker_name}-config-${formatdate("YYYYMMDDHHmmss", timestamp())}"

  production_variants {
    variant_name           = "default"
    model_name             = aws_sagemaker_model.llm.name
    initial_instance_count = var.sagemaker_initial_instance_count
    instance_type          = var.sagemaker_instance_type
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_sagemaker_endpoint" "llm_endpoint" {
  name                 = "${var.sagemaker_name}-endpoint"
  endpoint_config_name = aws_sagemaker_endpoint_configuration.llm_endpoint_configuration.name
}
