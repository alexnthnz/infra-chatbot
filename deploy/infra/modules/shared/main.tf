module "vpc" {
  source = "./modules/vpc"

  vpc_name   = var.vpc_name
  cidr_block = var.cidr_block
}

module "aurora" {
  source = "./modules/aurora"

  vpc_id              = module.vpc.vpc_id
  database_subnet_ids = module.vpc.vpc_public_subnets

  aurora_name            = var.aurora_name
  aurora_master_username = var.aurora_master_username

  depends_on = [module.vpc]
}
