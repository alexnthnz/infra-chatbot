module "secret_manager" {
  source = "./modules/secret_manager"

  secret_name = var.secret_name
}

module "iam" {
  source = "./modules/iam"

  lambda_function_name = var.lambda_function_name
  lambda_function_s3_bucket_arn = var.lambda_function_s3_bucket_arn

  aurora_cluster_arn = var.aurora_cluster_arn

  file_s3_bucket_arn = var.file_s3_bucket_arn

  secret_arn = module.secret_manager.secret_arn
}
