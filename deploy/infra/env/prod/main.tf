module "shared" {
  source = "../../modules/shared"

  vpc_name   = var.vpc_name
  cidr_block = var.cidr_block

  aurora_name            = var.aurora_name
  aurora_master_username = var.aurora_master_username

  bastion_name            = var.bastion_name
  ec2_bastion_ingress_ips = var.ec2_bastion_ingress_ips
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
