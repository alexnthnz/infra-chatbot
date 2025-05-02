resource "null_resource" "setup_database" {
  triggers = {
    always_run = "${timestamp()}"
  }
  connection {
    type        = "ssh"
    user        = "ec2-user"
    private_key = file(var.bastion_private_key_path)
    host        = var.bastion_public_ip
  }

  provisioner "file" {
    content = <<-EOT
      #!/bin/bash
      set -e  # Exit on error

      if ! command -v psql &> /dev/null; then
          echo "psql not found, installing..."
          sudo yum install -y postgresql
      fi

      echo "Running database setup..."

      export PGPASSWORD='${jsondecode(data.aws_secretsmanager_secret_version.this.secret_string)["password"]}'

      psql -h ${var.aurora_cluster_endpoint} \
           -p ${var.aurora_cluster_port} \
           -U ${var.aurora_cluster_master_username} \
           -d bedrock_kb <<SQL
CREATE EXTENSION IF NOT EXISTS vector;
CREATE SCHEMA IF NOT EXISTS bedrock_integration;
CREATE ROLE IF NOT EXISTS bedrock_user WITH LOGIN PASSWORD '${jsondecode(data.aws_secretsmanager_secret_version.this.secret_string)["password"]}';
GRANT ALL ON SCHEMA bedrock_integration TO bedrock_user;
CREATE TABLE IF NOT EXISTS bedrock_integration.bedrock_kb (
    id uuid PRIMARY KEY,
    embedding vector(1024),
    chunks text,
    metadata json,
    custom_metadata jsonb
);
CREATE INDEX ON bedrock_integration.bedrock_kb USING hnsw (embedding vector_cosine_ops) WITH (ef_construction=256);
CREATE INDEX ON bedrock_integration.bedrock_kb USING gin (to_tsvector('simple', chunks));
CREATE INDEX ON bedrock_integration.bedrock_kb USING gin (custom_metadata);
SQL
    EOT

    destination = "/tmp/setup_database.sh"
  }

  provisioner "remote-exec" {
    inline = [
      "chmod +x /tmp/setup_database.sh",
      "/tmp/setup_database.sh || { echo 'Database setup failed'; exit 1; }",
      "rm /tmp/setup_database.sh"
    ]
  }
}

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

  depends_on = [null_resource.setup_database]
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
