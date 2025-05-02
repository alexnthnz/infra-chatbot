output "bastion_public_ip" {
  description = "The public IP address of the bastion host"
  value       = aws_instance.bastion.public_ip
}

output "bastion_instance_id" {
  description = "The ID of the bastion host EC2 instance"
  value       = aws_instance.bastion.id
}

output "bastion_security_group_id" {
  description = "The ID of the security group attached to the bastion host"
  value       = aws_security_group.bastion.id
}

output "private_key_path" {
  description = "The path to the private key file for SSH access"
  value       = local_file.ec2-bastion-private-key.filename
  sensitive   = true
}

output "public_key_path" {
  description = "The path to the public key file for reference"
  value       = local_file.ec2-bastion-public-key.filename
}
