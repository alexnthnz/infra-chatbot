resource "null_resource" "setup_tools" {
  connection {
    type        = "ssh"
    user        = "ec2-user"
    private_key = file(local_file.ec2-bastion-private-key.filename)
    host        = aws_eip.bastion_eip.public_ip
  }

  provisioner "file" {
    source      = "./scripts/setup_tools.sh"
    destination = "/tmp/install_psql.sh"
  }

  provisioner "remote-exec" {
    inline = [
      "chmod +x /tmp/install_psql.sh",
      "sudo /tmp/install_psql.sh",
      "rm /tmp/install_psql.sh"
    ]
  }

  depends_on = [aws_instance.bastion, aws_eip.bastion_eip]
}
