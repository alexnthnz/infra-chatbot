module security_group_postgres {
  source  = "terraform-aws-modules/security-group/aws"
  version = "5.3.0"

  name        = "${var.project}-${var.environment}-postgres-sg"
  description = "Complete PostgreSQL security group"
  vpc_id      = module.vpc.vpc_id

  # ingress
  ingress_with_cidr_blocks = [
    {
      from_port   = var.rds_postgres_port
      to_port     = var.rds_postgres_port
      protocol    = "tcp"
      description = "PostgreSQL access from within VPC"
      cidr_blocks = module.vpc.vpc_cidr_block
    },
  ]

  depends_on = [ module.vpc ]
}

module security_group_redis {
  source  = "terraform-aws-modules/security-group/aws"
  version = "5.3.0"

  name        = "${var.project}-redis-sg"
  description = "Security group for ElastiCache Redis cluster"
  vpc_id      = module.vpc.vpc_id

  # ingress
  ingress_with_cidr_blocks = [
    {
      from_port   = var.elasticache_redis_port
      to_port     = var.elasticache_redis_port
      protocol    = "tcp"
      description = "Redis access from within VPC"
      cidr_blocks = module.vpc.vpc_cidr_block
    },
  ]

  depends_on = [module.vpc]
}
