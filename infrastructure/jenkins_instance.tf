terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "4.13.0"
    }
  }
}

resource "aws_instance" "jenkins_instance" {
  ami                    = "ami-0022f774911c1d690"
  instance_type          = "t2.medium"
  key_name               = "sethu"
  vpc_security_group_ids = [aws_security_group.security_jenkins_group.id]
  tags = {
    Name = "Jenkins Server"
  }

  connection {
    type    = "ssh"
    host    = self.public_ip
    user    = "ubuntu"
    timeout = "4m"
  }
}
resource "aws_security_group" "security_jenkins_group" {
  name        = "jenkins_sg_group"
  description = "security group for jenkins"

  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "my-jenkins-security-group"
  }
}

resource "aws_eip" "jenkins_elastic_ip" {
  vpc      = true
  instance = aws_instance.jenkins_instance.id
  tags = {
    Name = "jenkins_elastic_ip"
  }
}
