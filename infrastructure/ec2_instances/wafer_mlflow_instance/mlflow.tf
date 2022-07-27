provider "aws" {
  region = var.aws_region
}

resource "aws_instance" "mlflow_instance" {
  ami                    = var.mlflow_ami
  instance_type          = var.mlflow_instance_type
  key_name               = var.mlflow_key_pair_name
  vpc_security_group_ids = [aws_security_group.mlflow_security_group.id]
  tags = {
    Name = var.mlflow_tag_name
  }

  root_block_device {
    volume_size = var.mlflow_volume_size
    volume_type = var.mlflow_volume_type
    encrypted   = var.mlflow_volume_encryption
  }

  connection {
    type    = "ssh"
    host    = self.public_ip
    user    = "ubuntu"
    timeout = "4m"
  }
}

resource "aws_security_group" "mlflow_security_group" {
  name        = var.mlflow_sg_group_name
  description = "Security Group for MLFlow Server"

  ingress {
    from_port   = var.mlflow_ingress_from_port[0]
    to_port     = var.mlflow_ingress_to_port[0]
    protocol    = var.mlflow_protocol
    cidr_blocks = var.mlflow_cidr_block
  }

  ingress {
    from_port   = var.mlflow_ingress_from_port[1]
    to_port     = var.mlflow_ingress_to_port[1]
    protocol    = var.mlflow_protocol
    cidr_blocks = var.mlflow_cidr_block
  }

  ingress {
    from_port   = var.mlflow_ingress_from_port[2]
    to_port     = var.mlflow_ingress_to_port[2]
    protocol    = var.mlflow_protocol
    cidr_blocks = var.mlflow_cidr_block
  }

  ingress {
    from_port   = var.mlflow_ingress_from_port[3]
    to_port     = var.mlflow_ingress_to_port[3]
    protocol    = var.mlflow_protocol
    cidr_blocks = var.mlflow_cidr_block
  }

  egress {
    from_port   = var.mlflow_egress_from_port
    to_port     = var.mlflow_egress_to_port
    protocol    = var.mlflow_protocol
    cidr_blocks = var.mlflow_cidr_block
  }

  tags = {
    Name = var.mlflow_sg_group_name
  }

}

resource "aws_eip" "mlflow_elastic_ip" {
  vpc      = true
  instance = aws_instance.mlflow_instance.id
  tags = {
    Name = var.mlflow_eip_name
  }
}
