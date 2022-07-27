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