provider "aws" {
  region = var.aws_region
}

resource "aws_instance" "jenkins_instance" {
  ami                    = var.jenkins_ami
  instance_type          = var.jenkins_instance_type
  key_name               = var.jenkins_key_pair_name
  vpc_security_group_ids = [aws_security_group.jenkins_security_group.id]
  tags = {
    Name = var.tag_name
  }

  root_block_device {
    volume_size = var.jenkins_volume_size 
    volume_type = var.jenkins_volume_type
    encrypted   = var.jenkins_volume_encryption
  }

  connection {
    type    = "ssh"
    host    = self.public_ip
    user    = "ubuntu"
    timeout = "4m"
  }
}

resource "aws_security_group" "jenkins_security_group" {
  name        = var.jenkins_sg_group_name
  description = "Security Group for Jenkins Server"

  ingress {
    from_port   = var.jenkins_ingress_from_port[0]
    to_port     = var.jenkins_ingress_to_port[0]
    protocol    = var.jenkins_protocol
    cidr_blocks = var.jenkins_cidr_block
  }

  ingress {
    from_port   = var.jenkins_ingress_from_port[1]
    to_port     = var.jenkins_ingress_to_port[1]
    protocol    = var.jenkins_protocol
    cidr_blocks = var.jenkins_cidr_block
  }

  egress {
    from_port   = var.jenkins_egress_from_port
    to_port     = var.jenkins_egress_to_port
    protocol    = var.jenkins_protocol
    cidr_blocks = var.jenkins_cidr_block
  }

  tags = {
    Name = var.jenkins_sg_group_name
  }
}

resource "aws_eip" "elastic_ip" {
  vpc      = true
  instance = aws_instance.jenkins_instance.id
  tags = {
    Name = var.jenkins_eip_name
  }
}
