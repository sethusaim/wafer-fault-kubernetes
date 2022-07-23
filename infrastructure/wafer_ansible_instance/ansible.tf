provider "aws" {
  region = var.aws_region
}

resource "aws_instance" "ansible_instance" {
  ami                    = var.ansible_ami
  instance_type          = var.ansible_instance_type
  key_name               = var.ansible_key_pair_name
  vpc_security_group_ids = [aws_security_group.security_group.id]
  tags = {
    Name = var.ansible_tag_name
  }

  root_block_device {
    volume_size = var.ansible_volume_size
    volume_type = var.ansible_volume_type
    encrypted   = var.ansible_volume_encryption
  }

  connection {
    type    = "ssh"
    host    = self.public_ip
    user    = "ubuntu"
    timeout = "4m"
  }
}

resource "aws_security_group" "security_group" {
  name        = var.ansible_sg_group_name
  description = "Security Group for EKS Master Server"

  ingress {
    from_port   = var.ansible_ingress_from_port
    to_port     = var.ansible_ingress_to_port
    protocol    = var.ansible_protocol
    cidr_blocks = var.ansible_cidr_block
  }

  egress {
    from_port   = var.ansible_egress_from_port
    to_port     = var.ansible_egress_to_port
    protocol    = var.ansible_protocol
    cidr_blocks = var.ansible_cidr_block
  }

  tags = {
    Name = var.ansible_sg_group_name
  }
}

resource "aws_eip" "elastic_ip" {
  vpc      = true
  instance = aws_instance.ansible_instance.id
  tags = {
    Name = var.ansible_eip_name
  }
}