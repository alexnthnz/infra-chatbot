module "shared" {
  source = "../../modules/shared"

  vpc_name   = var.vpc_name
  cidr_block = var.cidr_block

  aurora_name            = var.aurora_name
  aurora_master_username = var.aurora_master_username
}

module "llm_rag" {
  source = "../../modules/llm_rag"

  aurora_cluster_arn             = module.shared.aurora_cluster_arn
  aurora_cluster_endpoint        = module.shared.aurora_cluster_endpoint
  aurora_cluster_port            = module.shared.aurora_cluster_port
  aurora_cluster_master_username = module.shared.aurora_cluster_master_username
  aurora_cluster_resource_id     = module.shared.aurora_cluster_resource_id
  aurora_secret_arn              = module.shared.aurora_cluster_master_user_secret[0].secret_arn

  kb_name                  = var.kb_name
  kb_model_id              = var.kb_model_id
  kb_s3_bucket_name_prefix = var.kb_s3_bucket_name_prefix

  sagemaker_name                   = var.sagemaker_name
  sagemaker_instance_type          = var.sagemaker_instance_type
  sagemaker_initial_instance_count = var.sagemaker_initial_instance_count
  sagemaker_ecr_image_uri          = var.sagemaker_ecr_image_uri

  depends_on = [module.shared]
}
