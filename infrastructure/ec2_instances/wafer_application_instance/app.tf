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