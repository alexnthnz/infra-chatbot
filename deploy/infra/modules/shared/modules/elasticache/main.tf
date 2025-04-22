module "elasticache" {
  source = "terraform-aws-modules/elasticache/aws"
  version = "1.6.0"

  cluster_id               = "${var.project}-${var.environment}-redis"
  create_cluster           = true
  create_replication_group = false

  engine_version = "7.1"
  node_type      = var.elasticache_redis_instance_type
  engine         = "redis" 

  maintenance_window = "sun:05:00-sun:09:00"
  apply_immediately  = true

  # Security Group
  vpc_id = module.vpc.vpc_id
  security_group_ids = [module.security_group_redis.security_group_id] 

  # Subnet Group
  subnet_group_name        = module.vpc.database_subnet_group_name
  subnet_group_description = "${title(module.vpc.database_subnet_group_name)} subnet group"
  subnet_ids               = module.vpc.private_subnets

  # Parameter Group
  create_parameter_group      = true
  parameter_group_name        = "${var.project}-${var.environment}-redis-parameter-group"
  parameter_group_family      = "redis7"
  parameter_group_description = "${var.project}-${var.environment}-redis-parameter-group parameter group"
  parameters = [
    {
      name  = "latency-tracking"
      value = "yes"
    }
  ]

  timeouts = {
    create = "1h"
    update = "2h"
    delete = "1h"
  }
}
