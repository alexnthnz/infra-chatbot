module "shared" {
  source = "../../modules/shared"

  vpc_name   = var.vpc_name
  cidr_block = var.cidr_block

  aurora_name            = var.aurora_name
  aurora_master_username = var.aurora_master_username

  bastion_name            = var.bastion_name
  ec2_bastion_ingress_ips = var.ec2_bastion_ingress_ips

  s3_bucket_handler_name = var.s3_bucket_handler_name

  elasticache_name = var.elasticache_name

  secret_name = var.secret_name
}

module "llm_rag" {
  source = "../../modules/llm_rag"

  aurora_cluster_arn = module.shared.aurora_cluster_arn
  aurora_secret_arn  = module.shared.aurora_cluster_master_user_secret[0].secret_arn

  kb_name                  = var.kb_name
  kb_model_id              = var.kb_model_id
  kb_s3_bucket_name_prefix = var.kb_s3_bucket_name_prefix

  depends_on = [module.shared]
}

module "handler" {
  source = "../../modules/handler"

  lambda_function_name               = var.lambda_function_handler_name
  lambda_function_s3_bucket_arn      = var.lambda_function_handler_s3_bucket_arn
  lambda_function_s3_bucket_name     = var.lambda_function_handler_s3_bucket_name
  lambda_zip_key                     = var.lambda_function_handler_zip_key
  lambda_function_subnet_ids         = module.shared.vpc_public_subnet_ids
  lambda_function_security_group_ids = [module.shared.aurora_cluster_security_group_id, module.shared.elasticache_security_group_id]

  aurora_cluster_arn = module.shared.aurora_cluster_arn

  file_s3_bucket_arn = module.shared.file_s3_bucket_arn

  secret_arn = module.shared.secret_arn

  stage_name = "prod"
}
