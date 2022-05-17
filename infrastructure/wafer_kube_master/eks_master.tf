provider "aws" {
  region = var.aws_region
}

resource "aws_instance" "eks_master_instance" {
  ami                    = var.eks_master_ami
  instance_type          = var.eks_master_instance_type
  key_name               = var.eks_master_key_pair_name
  vpc_security_group_ids = [aws_security_group.security_group.id]
  tags = {
    Name = var.eks_master_tag_name
  }

  root_block_device {
    volume_size = var.eks_master_volume_size
    volume_type = var.eks_master_volume_type
    encrypted   = var.eks_master_volume_encryption
  }

  connection {
    type    = "ssh"
    host    = self.public_ip
    user    = "ubuntu"
    timeout = "4m"
  }
}

resource "aws_security_group" "security_group" {
  name        = var.eks_master_sg_group_name
  description = "Security Group for EKS Master Server"

  ingress {
    from_port   = var.eks_master_ingress_from_port[0]
    to_port     = var.eks_master_ingress_to_port[0]
    protocol    = var.eks_master_protocol
    cidr_blocks = var.eks_master_cidr_block
  }

  ingress {
    from_port   = var.eks_master_ingress_from_port[1]
    to_port     = var.eks_master_ingress_to_port[1]
    protocol    = var.eks_master_protocol
    cidr_blocks = var.eks_master_cidr_block
  }

  egress {
    from_port   = var.eks_master_egress_from_port
    to_port     = var.eks_master_egress_to_port
    protocol    = var.eks_master_protocol
    cidr_blocks = var.eks_master_cidr_block
  }

  tags = {
    Name = var.eks_master_sg_group_name
  }
}

resource "aws_eip" "elastic_ip" {
  vpc      = true
  instance = aws_instance.eks_master_instance.id
  tags = {
    Name = var.eks_master_eip_name
  }
}
