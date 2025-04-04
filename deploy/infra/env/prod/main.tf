module "shared" {
  source = "../../modules/shared"

  agent_model_role_name       = var.agent_model_role_name 
  foundation_model_role_name  = var.foundation_model_role_name 
  model_artifacts_bucket_name = var.model_artifacts_bucket_name
  aws_region                  = var.aws_region
}

module "agent" {
  source = "../../modules/agent_model"

  model_name            = var.agent_model_name
  execution_role_arn    = module.shared.agent_model_role_arn
  ecr_image_uri         = var.agent_ecr_image_uri
  instance_type         = var.agent_instance_type
  initial_instance_count = var.agent_initial_instance_count
}
