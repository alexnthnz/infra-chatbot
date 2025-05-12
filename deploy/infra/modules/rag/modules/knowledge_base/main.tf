resource "aws_bedrockagent_knowledge_base" "llm_kb" {
  name     = var.kb_name
  role_arn = var.bedrock_role_arn
  knowledge_base_configuration {
    vector_knowledge_base_configuration {
      embedding_model_arn = var.kb_model_arn
    }
    type = "VECTOR"
  }
  storage_configuration {
    type = "RDS"
    rds_configuration {
      database_name          = "bedrock_kb"
      credentials_secret_arn = var.aurora_secret_arn
      table_name             = "bedrock_integration.bedrock_kb"
      resource_arn           = var.aurora_cluster_arn

      field_mapping {
        primary_key_field = "id"
        vector_field      = "embedding"
        text_field        = "chunks"
        metadata_field    = "metadata"
      }
    }
  }
}

resource "aws_bedrockagent_data_source" "llm_kb" {
  knowledge_base_id = aws_bedrockagent_knowledge_base.llm_kb.id
  name              = "${var.kb_name}DataSource"
  data_source_configuration {
    type = "S3"
    s3_configuration {
      bucket_arn = var.s3_arn
    }
  }
}
