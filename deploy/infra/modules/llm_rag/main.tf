module "s3_bucket" {
  source      = "./modules/s3"
  bucket_name = "${var.kb_s3_bucket_name_prefix}-${local.region_short}-${local.account_id}"
}

module "iam" {
  source             = "./modules/iam"
  kb_name            = var.kb_name
  s3_arn             = module.s3_bucket.arn
  kb_model_arn       = data.aws_bedrock_foundation_model.kb.model_arn
  aurora_cluster_arn = var.aurora_cluster_arn
  aurora_secret_arn  = var.aurora_secret_arn
  sagemaker_name     = var.sagemaker_name
}

module "knowledge_base" {
  source = "./modules/knowledge_base"

  aurora_cluster_arn         = var.aurora_cluster_arn
  aurora_cluster_resource_id = var.aurora_cluster_resource_id
  aurora_secret_arn          = var.aurora_secret_arn

  kb_name           = var.kb_name
  bedrock_role_arn  = module.iam.bedrock_role_arn
  bedrock_role_name = module.iam.bedrock_role_name
  kb_model_arn      = data.aws_bedrock_foundation_model.kb.model_arn

  s3_arn = module.s3_bucket.arn
}
