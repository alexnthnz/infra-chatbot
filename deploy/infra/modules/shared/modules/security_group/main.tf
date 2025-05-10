module "vpc_endpoint_security_group" {
  source  = "terraform-aws-modules/security-group/aws"
  version = "5.3.0"

  name        = "vpc-endpoint-sg"
  description = "Allow VPC endpoint to access Secrets Manager"
  vpc_id      = var.vpc_id

  ingress_with_cidr_blocks = [
    {
      description = "Allow all inbound traffic from VPC CIDR"
      from_port   = 443
      to_port     = 443
      protocol    = "tcp"
      cidr_blocks = "0.0.0.0/0"
    },
  ]

  egress_with_cidr_blocks = [
    {
      description = "Allow all outbound traffic"
      from_port   = 0
      to_port     = 0
      protocol    = "-1"
      cidr_blocks = "0.0.0.0/0"
    }
  ]
}

module "lambda_sg" {
  source  = "terraform-aws-modules/security-group/aws"
  version = "5.3.0"

  name        = "lambda-to-resources-sg"
  description = "Allow lambda outbound to DB & AWS APIs"
  vpc_id      = var.vpc_id

  computed_ingress_with_source_security_group_id = concat(
    [
      {
        source_security_group_id = var.aurora_security_group_id
        description              = "Allow Lambda to access Aurora PostgreSQL"
        to_port                  = 5432
        from_port                = 5432
        protocol                 = "tcp"
      },
      {
        source_security_group_id = module.vpc_endpoint_security_group.security_group_id
        description              = "Allow Lambda to access Secrets Manager"
        to_port                  = 443
        from_port                = 443
        protocol                 = "tcp"
      },
    ],
    var.elasticache_security_group_id != null ? [
      {
        source_security_group_id = var.elasticache_security_group_id
        description              = "Allow Lambda to access ElastiCache"
        to_port                  = 6379
        from_port                = 6379
        protocol                 = "tcp"
      },
    ] : []
  )

  egress_with_cidr_blocks = [
    {
      description = "Allow all outbound traffic"
      from_port   = 0
      to_port     = 0
      protocol    = "-1"
      cidr_blocks = "0.0.0.0/0"
    },
  ]
}
