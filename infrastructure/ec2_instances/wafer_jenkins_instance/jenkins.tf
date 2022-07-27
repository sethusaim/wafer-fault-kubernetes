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