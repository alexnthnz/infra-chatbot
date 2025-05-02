resource "tls_private_key" "ec2-bastion-host-key-pair" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "local_file" "ec2-bastion-public-key" {
  depends_on = [tls_private_key.ec2-bastion-host-key-pair]
  filename   = "${var.key_pair_path}/public-key.pem"
  content    = tls_private_key.ec2-bastion-host-key-pair.public_key_openssh
}

resource "local_file" "ec2-bastion-private-key" {
  depends_on = [tls_private_key.ec2-bastion-host-key-pair]
  filename   = "${var.key_pair_path}/private-key.pem"
  content    = tls_private_key.ec2-bastion-host-key-pair.private_key_pem
}

resource "aws_key_pair" "ec2-bastion-host-key-pair" {
  depends_on = [local_file.ec2-bastion-public-key]
  key_name   = "ec2-bastion-host-key-pair"
  public_key = tls_private_key.ec2-bastion-host-key-pair.public_key_openssh
}

resource "aws_security_group" "bastion" {
  description = "EC2 Bastion Host Security Group"
  name        = "${var.bastion_name}-ec2-bastion-sg"
  vpc_id      = var.vpc_id
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = var.ec2_bastion_ingress_ips
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group_rule" "aurora_ingress" {
  type                     = "ingress"
  from_port                = 5432
  to_port                  = 5432
  protocol                 = "tcp"
  security_group_id        = var.aurora_security_group_id
  source_security_group_id = aws_security_group.bastion.id
}

resource "aws_instance" "bastion" {
  ami                         = data.aws_ami.amazon_linux.id
  instance_type               = "t3.micro"
  subnet_id                   = var.public_subnet_id
  key_name                    = aws_key_pair.ec2-bastion-host-key-pair.key_name
  vpc_security_group_ids      = [aws_security_group.bastion.id]
  associate_public_ip_address = false

  tags = { Name = "${var.bastion_name}-bastion" }

  lifecycle {
    ignore_changes = [
      associate_public_ip_address,
    ]
  }
}

resource "aws_eip" "bastion_eip" {
  instance = aws_instance.bastion.id
  tags     = { Name = "${var.bastion_name}-bastion-eip" }
}
