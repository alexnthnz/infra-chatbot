resource "null_resource" "setup_database" {
  triggers = {
    always_run = "${timestamp()}"
  }
  connection {
    type        = "ssh"
    user        = "ec2-user"
    private_key = file(local_file.ec2-bastion-private-key.filename)
    host        = aws_instance.bastion.public_ip
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
CREATE EXTENSION vector;
CREATE SCHEMA bedrock_integration;
CREATE ROLE bedrock_user WITH LOGIN PASSWORD '${jsondecode(data.aws_secretsmanager_secret_version.this.secret_string)["password"]}';
GRANT ALL ON SCHEMA bedrock_integration TO bedrock_user;
CREATE TABLE bedrock_integration.bedrock_kb (
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

  depends_on = [aws_instance.bastion]
}
