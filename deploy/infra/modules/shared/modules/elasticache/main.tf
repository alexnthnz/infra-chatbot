module "security_group_redis" {
  source  = "terraform-aws-modules/security-group/aws"
  version = "5.3.0"

  name        = "${var.elasticache_name}-redis-sg"
  description = "Security group for ElastiCache Redis cluster"
  vpc_id      = var.vpc_id

  # ingress
  ingress_with_cidr_blocks = [
    {
      from_port   = 6379
      to_port     = 6379
      protocol    = "tcp"
      description = "Redis access from within VPC"
      cidr_blocks = var.vpc_cidr_block
    },
  ]
}

resource "aws_elasticache_serverless_cache" "redis_serverless_cache" {
  engine = "redis"
  name   = var.elasticache_name
  cache_usage_limits {
    data_storage {
      maximum = 5
      unit    = "GB"
    }
    ecpu_per_second {
      maximum = 5000
    }
  }

  daily_snapshot_time      = "00:00"
  description              = "${var.elasticache_name} ElastiCache Redis Serverless"
  major_engine_version     = "7"
  snapshot_retention_limit = 1
  security_group_ids       = [module.security_group_redis.security_group_id]
  subnet_ids               = var.vpc_subnet_ids
}
