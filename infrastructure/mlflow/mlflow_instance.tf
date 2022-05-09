resource "aws_instance" "instance" {
  ami                    = var.ami
  instance_type          = var.instance_type
  key_name               = var.key_pair_name
  vpc_security_group_ids = [aws_security_group.security_group.id]
  tags = {
    Name = var.tag_name
  }

  connection {
    type    = "ssh"
    host    = self.public_ip
    user    = "ubuntu"
    timeout = "4m"
  }
}

resource "aws_security_group" "security_group" {
  name        = var.sg_group_name
  description = "Security Group for MLFlow Server"

  ingress {
    from_port   = var.ingress_from_port[0]
    to_port     = var.ingress_to_port[0]
    protocol    = var.protocol
    cidr_blocks = var.ingress_cidr
  }

  ingress {
    from_port   = var.ingress_from_port[1]
    to_port     = var.ingress_to_port[1]
    protocol    = var.protocol
    cidr_blocks = var.ingress_cidr
  }

  ingress {
    from_port   = var.ingress_from_port[2]
    to_port     = var.ingress_to_port[2]
    protocol    = var.protocol
    cidr_blocks = var.ingress_cidr
  }

  ingress {
    from_port   = var.ingress_from_port[3]
    to_port     = var.ingress_to_port[3]
    protocol    = var.protocol
    cidr_blocks = var.ingress_cidr
  }


  egress {
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "MLFlow-Security-Group"
  }
}

resource "aws_eip" "elastic_ip" {
  vpc      = true
  instance = aws_instance.instance.id
  tags = {
    Name = "Elastic_IP"
  }
}
