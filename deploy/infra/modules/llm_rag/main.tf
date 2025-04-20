module "s3_bucket" {
  source      = "./modules/s3"
  bucket_name = "${var.kb_s3_bucket_name_prefix}-${local.region_short}-${local.account_id}"
}

module "iam" {
  source              = "./modules/iam"
  kb_name             = var.kb_name
  s3_arn              = module.s3_bucket.arn
  kb_model_arn        = data.aws_bedrock_foundation_model.kb.model_arn
}

module "opensearch" {
  source                 = "./modules/opensearch"
  kb_oss_collection_name = var.kb_oss_collection_name
  bedrock_role_arn       = module.iam.bedrock_role_arn
  index_name             = "bedrock-knowledge-base-default-index"
}

resource "time_sleep" "delay" {
  depends_on      = [module.opensearch.opensearch_index_name]
  create_duration = "60s"
}

module "knowledge_base" {
  source                = "./modules/knowledge_base"
  kb_name               = var.kb_name
  bedrock_role_arn      = module.iam.bedrock_role_arn
  bedrock_role_name     = module.iam.bedrock_role_name
  kb_model_arn          = data.aws_bedrock_foundation_model.kb.model_arn
  opensearch_arn        = module.opensearch.opensearch_collection_arn
  s3_arn                = module.s3_bucket.arn
  opensearch_index_name = module.opensearch.opensearch_index_name
  depends_on            = [time_sleep.delay]
}
