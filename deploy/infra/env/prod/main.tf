# module "shared" {
#   source = "../../modules/shared"
#
#   agent_model_role_name       = var.agent_model_role_name
#   foundation_model_role_name  = var.foundation_model_role_name
#   model_artifacts_bucket_name = var.model_artifacts_bucket_name
#   aws_region                  = var.aws_region
#   project                     = var.project
#   cidr_block                  = var.cidr_block
#   environment                 = var.environment
#
#   rds_postgres_db_name        = var.rds_postgres_db_name
#   rds_postgres_username       = var.rds_postgres_username
#   rds_postgres_password       = var.rds_postgres_password
#   rds_postgres_instance_type  = var.rds_postgres_instance_type
#   rds_postgres_port           = var.rds_postgres_port
#
#   elasticache_redis_port      = var.elasticache_redis_port
#   elasticache_redis_instance_type = var.elasticache_redis_instance_type
# }
#
# module "agent" {
#   source = "../../modules/agent_model"
#
#   model_name             = var.agent_model_name
#   execution_role_arn     = module.shared.agent_model_role_arn
#   ecr_image_uri          = var.agent_ecr_image_uri
#   instance_type          = var.agent_instance_type
#   initial_instance_count = var.agent_initial_instance_count
# }

module "llm_rag" {
  source = "../../modules/llm_rag"
}
