# module "security_group_postgres" {
#   source  = "terraform-aws-modules/security-group/aws"
#   version = "5.3.0"
#
#   name        = "${var.project}-${var.environment}-postgres-sg"
#   description = "Complete PostgreSQL security group"
#   vpc_id      = module.vpc.vpc_id
#
#   # ingress
#   ingress_with_cidr_blocks = [
#     {
#       from_port   = var.rds_postgres_port
#       to_port     = var.rds_postgres_port
#       protocol    = "tcp"
#       description = "PostgreSQL access from within VPC"
#       cidr_blocks = module.vpc.vpc_cidr_block
#     },
#   ]
#
#   depends_on = [module.vpc]
# }


