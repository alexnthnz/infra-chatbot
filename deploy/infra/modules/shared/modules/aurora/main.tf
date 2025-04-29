resource "aws_db_subnet_group" "aurora_public" {
  name       = "${var.aurora_name}-public-subnet-group"
  subnet_ids = var.database_subnet_ids
}

module "aurora" {
  source  = "terraform-aws-modules/rds-aurora/aws"
  version = "9.13.0"

  # Cluster Configuration
  name                = var.aurora_name
  engine              = "aurora-postgresql"
  engine_version      = "16.6"
  engine_mode         = "provisioned"
  master_username     = var.aurora_master_username
  master_password     = var.aurora_master_password
  publicly_accessible = true

  iam_database_authentication_enabled = true
  enable_http_endpoint                = true

  database_name  = "bedrock_kb"
  instance_class = "db.serverless"
  instances = {
    one = {}
    two = {}
  }

  # Serverless v2 Scaling
  serverlessv2_scaling_configuration = {
    min_capacity             = 0
    max_capacity             = 2
    seconds_until_auto_pause = 3600
  }

  # Network Configuration
  vpc_id               = var.vpc_id
  db_subnet_group_name = aws_db_subnet_group.aurora_public.name
  security_group_rules = {
    all_ingress = {
      cidr_blocks = ["0.0.0.0/0"] # Open to all IPs
      description = "PostgreSQL from any IP (dev only)"
    }
    egress_all = {
      type        = "egress"
      cidr_blocks = ["0.0.0.0/0"]
      description = "Allow all outbound"
    }
  }

  # Lifecycle and Snapshots
  apply_immediately            = true
  skip_final_snapshot          = true
  backup_retention_period      = 1
  preferred_backup_window      = "03:00-04:00"
  preferred_maintenance_window = "sun:05:00-sun:06:00"

  # Parameter Groups
  create_db_cluster_parameter_group      = true
  db_cluster_parameter_group_name        = "${var.aurora_name}-dev-cluster"
  db_cluster_parameter_group_family      = "aurora-postgresql16"
  db_cluster_parameter_group_description = "${var.aurora_name} dev cluster parameter group"
  db_cluster_parameter_group_parameters = [
    {
      name         = "log_min_duration_statement"
      value        = 1000
      apply_method = "immediate"
    }
  ]

  # Tags
  tags = {
    Environment = "dev"
    Purpose     = "bedrock-knowledge-base"
  }
}
