resource "null_resource" "setup_database" {
  triggers = {
    run_once = "true"
  }
  connection {
    type        = "ssh"
    user        = "ec2-user"
    private_key = file(local_file.ec2-bastion-private-key.filename)
    host        = aws_eip.bastion_eip.public_ip
  }

  provisioner "file" {
    content = templatefile("./scripts/setup_bedrock_db.sh.tmpl", {
      password        = jsondecode(data.aws_secretsmanager_secret_version.this.secret_string)["password"]
      aurora_endpoint = var.aurora_cluster_endpoint
      aurora_port     = var.aurora_cluster_port
      aurora_username = var.aurora_cluster_master_username
    })
    destination = "/tmp/setup_database.sh"
  }

  provisioner "remote-exec" {
    inline = [
      "chmod +x /tmp/setup_database.sh",
      "/tmp/setup_database.sh || { echo 'Database setup failed'; exit 1; }",
      "rm /tmp/setup_database.sh"
    ]
  }

  lifecycle {
    ignore_changes = [triggers]
  }

  depends_on = [aws_instance.bastion, aws_eip.bastion_eip, null_resource.setup_tools]
}
