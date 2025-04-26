module "rds_postgres" {
  source  = "terraform-aws-modules/rds/aws"
  version = "6.11.0"

  identifier = "${var.project}-${var.environment}-postgres"

  apply_immediately = true

  engine               = "postgres"
  engine_version       = "16"
  family               = "postgres14" # DB parameter group
  major_engine_version = "16"         # DB option group
  instance_class       = var.rds_postgres_instance_type

  allocated_storage     = 20
  max_allocated_storage = 100

  manage_master_user_password = false
  db_name                     = var.rds_postgres_db_name
  username                    = var.rds_postgres_username
  port                        = var.rds_postgres_port
  password                    = var.rds_postgres_password

  multi_az               = false
  db_subnet_group_name   = module.vpc.database_subnet_group
  vpc_security_group_ids = [module.security_group_postgres.security_group_id]

  publicly_accessible = false

  backup_retention_period = 1
  skip_final_snapshot     = true
  deletion_protection     = false

  maintenance_window              = "Mon:00:00-Mon:03:00"
  backup_window                   = "03:00-06:00"
  enabled_cloudwatch_logs_exports = ["postgresql", "upgrade"]
  create_cloudwatch_log_group     = true

  performance_insights_enabled          = true
  performance_insights_retention_period = 7
  create_monitoring_role                = true
  monitoring_interval                   = 60
  monitoring_role_name                  = "example-monitoring-role-name"
  monitoring_role_use_name_prefix       = true
  monitoring_role_description           = "Description for monitoring role"

  depends_on = [
    module.vpc,
    module.security_group_postgres,
  ]
}
