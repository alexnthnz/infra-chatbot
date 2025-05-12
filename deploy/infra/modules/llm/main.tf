module "iam" {
  source = "./modules/iam"

  sagemaker_name = var.sagemaker_name
}

module "sagemaker" {
  source = "./modules/sagemaker"

  sagemaker_name                   = var.sagemaker_name
  sagemaker_execution_role_arn     = module.iam.sagemaker_role_arn
  sagemaker_ecr_image_uri          = var.sagemaker_ecr_image_uri
  sagemaker_initial_instance_count = var.sagemaker_initial_instance_count
  sagemaker_instance_type          = var.sagemaker_instance_type
  sagemaker_hf_model_id            = var.sagemaker_hf_model_id
  sagemaker_hf_access_token        = var.sagemaker_hf_access_token
  sagemaker_tgi_config             = var.sagemaker_tgi_config
}
