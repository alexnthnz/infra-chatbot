module "shared" {
  source = "../../modules/shared"

  vpc_name   = var.vpc_name
  cidr_block = var.cidr_block

  aurora_name            = var.aurora_name
  aurora_master_username = var.aurora_master_username

  bastion_name            = var.bastion_name
  ec2_bastion_ingress_ips = var.ec2_bastion_ingress_ips

  s3_bucket_handler_name = var.s3_bucket_handler_name

  elasticache_enabled = var.elasticache_enabled
  elasticache_name    = var.elasticache_name

  secret_name = var.secret_name
}

module "llm" {
  source = "../../modules/llm"

  sagemaker_name                   = var.sagemaker_name
  sagemaker_ecr_image_uri          = var.sagemaker_ecr_image_uri
  sagemaker_initial_instance_count = var.sagemaker_initial_instance_count
  sagemaker_instance_type          = var.sagemaker_instance_type
  sagemaker_hf_model_id            = var.sagemaker_hf_model_id
  sagemaker_hf_access_token        = var.sagemaker_hf_access_token
  sagemaker_tgi_config             = var.sagemaker_tgi_config
}

module "rag" {
  source = "../../modules/rag"

  aurora_cluster_arn = module.shared.aurora_cluster_arn
  aurora_secret_arn  = module.shared.aurora_cluster_master_user_secret[0].secret_arn

  kb_name                  = var.kb_name
  kb_model_id              = var.kb_model_id
  kb_s3_bucket_name_prefix = var.kb_s3_bucket_name_prefix

  depends_on = [module.shared]
}

module "handler" {
  source = "../../modules/handler"

  vpc_id = module.shared.vpc_id

  lambda_function_ecr_image_uri     = var.lambda_function_ecr_image_uri
  lambda_function_name              = var.lambda_function_handler_name
  lambda_function_subnet_ids        = module.shared.vpc_private_subnet_ids
  lambda_function_security_group_id = module.shared.lambda_security_group_id

  aurora_cluster_arn = module.shared.aurora_cluster_arn

  file_s3_bucket_arn = module.shared.file_s3_bucket_arn

  secret_arn = module.shared.secret_arn

  stage_name = "prod"
}
