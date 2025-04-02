module "shared" {
  source = "../../modules/shared"

  agent_model_role_name       = var.agent_model_role_name 
  foundation_model_role_name  = var.foundation_model_role_name 
  model_artifacts_bucket_name = var.model_artifacts_bucket_name
}
