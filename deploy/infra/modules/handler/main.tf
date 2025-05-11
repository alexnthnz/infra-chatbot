module "iam" {
  source = "./modules/iam"

  lambda_function_name = var.lambda_function_name

  aurora_cluster_arn = var.aurora_cluster_arn

  file_s3_bucket_arn = var.file_s3_bucket_arn

  secret_arn = var.secret_arn
}

module "lambda" {
  source = "./modules/lambda"

  lambda_function_ecr_image_uri = var.lambda_function_ecr_image_uri
  lambda_role_arn               = module.iam.lambda_role_arn
  lambda_function_name          = var.lambda_function_name
  lambda_security_group_id      = var.lambda_function_security_group_id

  vpc_id     = var.vpc_id
  subnet_ids = var.lambda_function_subnet_ids

  secret_arn = var.secret_arn

}

module "apigw" {
  source = "./modules/api_gateway"

  api_gateway_name           = "${var.lambda_function_name}-apigw"
  lambda_function_name       = var.lambda_function_name
  lambda_function_invoke_arn = module.lambda.lambda_function_invoke_arn

  stage_name = var.stage_name
}
