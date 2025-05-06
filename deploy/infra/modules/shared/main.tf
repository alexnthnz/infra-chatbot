module "vpc" {
  source = "./modules/vpc"

  vpc_name   = var.vpc_name
  cidr_block = var.cidr_block
}

module "aurora" {
  source = "./modules/aurora"

  vpc_id              = module.vpc.vpc_id
  database_subnet_ids = module.vpc.vpc_database_subnets

  aurora_name            = var.aurora_name
  aurora_master_username = var.aurora_master_username

  depends_on = [module.vpc]
}

module "bastion" {
  source = "./modules/bastion"

  aurora_secret_arn              = module.aurora.cluster_master_user_secret[0].secret_arn
  aurora_cluster_endpoint        = module.aurora.cluster_endpoint
  aurora_cluster_master_username = module.aurora.cluster_master_username
  aurora_cluster_port            = module.aurora.cluster_port

  vpc_id                   = module.vpc.vpc_id
  public_subnet_id         = module.vpc.vpc_public_subnets[0]
  aurora_security_group_id = module.aurora.cluster_security_group_id
  bastion_name             = var.bastion_name
  ec2_bastion_ingress_ips  = var.ec2_bastion_ingress_ips

  depends_on = [module.vpc, module.aurora]
}

module "file_bucket" {
  source = "./modules/s3"

  s3_bucket_name = var.s3_bucket_handler_name
}

module "elasticache" {
  source = "./modules/elasticache"

  elasticache_name = var.elasticache_name
  vpc_id           = module.vpc.vpc_id
  vpc_cidr_block   = module.vpc.vpc_cidr_block
  vpc_subnet_ids   = module.vpc.vpc_database_subnets

  depends_on = [module.vpc]
}

module "secrets_manager" {
  source = "./modules/secrets_manager"

  secret_name = var.secret_name
}
