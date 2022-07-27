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