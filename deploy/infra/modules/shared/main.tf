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

  vpc_id                   = module.vpc.vpc_id
  public_subnet_id         = module.vpc.vpc_public_subnets[0]
  aurora_security_group_id = module.aurora.cluster_security_group_id
  bastion_name             = var.bastion_name
  ec2_bastion_ingress_ips  = var.ec2_bastion_ingress_ips

  depends_on = [module.vpc, module.aurora]
}
