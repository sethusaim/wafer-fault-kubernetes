provider "aws" {
  region = var.aws_region
}

resource "aws_instance" "application_instance" {
  ami                    = var.application_ami
  instance_type          = var.application_instance_type
  key_name               = var.application_key_pair_name
  vpc_security_group_ids = [aws_security_group.security_group.id]
  tags = {
    Name = var.application_tag_name
  }

  root_block_device {
    volume_size = var.application_volume_size
    volume_type = var.application_volume_type
    encrypted   = var.application_volume_encryption
  }

  connection {
    type    = "ssh"
    host    = self.public_ip
    user    = "ubuntu"
    timeout = "4m"
  }
}

resource "aws_security_group" "security_group" {
  name        = var.application_sg_group_name
  description = "Security Group for EKS Master Server"

  ingress {
    from_port   = var.application_ingress_from_port[0]
    to_port     = var.application_ingress_to_port[0]
    protocol    = var.application_protocol
    cidr_blocks = var.application_cidr_block
  }

  ingress {
    from_port   = var.application_ingress_from_port[1]
    to_port     = var.application_ingress_to_port[1]
    protocol    = var.application_protocol
    cidr_blocks = var.application_cidr_block
  }

  egress {
    from_port   = var.application_egress_from_port
    to_port     = var.application_egress_to_port
    protocol    = var.application_protocol
    cidr_blocks = var.application_cidr_block
  }

  tags = {
    Name = var.application_sg_group_name
  }
}

resource "aws_eip" "elastic_ip" {
  vpc      = true
  instance = aws_instance.application_instance.id
  tags = {
    Name = var.application_eip_name
  }
}
