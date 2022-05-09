terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "4.13.0"
    }
  }
}

resource "aws_instance" "mlflow_instance" {
  ami                    = "ami-0c4f7023847b90238"
  instance_type          = "t2.small"
  key_name               = "sethu"
  vpc_security_group_ids = [aws_security_group.security_mlflow_group.id]
  tags = {
    Name = "MLFlow Server"
  }

  connection {
    type    = "ssh"
    host    = self.public_ip
    user    = "ubuntu"
    timeout = "4m"
  }
}
resource "aws_security_group" "security_mlflow_group" {
  name        = "mlflow_sg_group"
  description = "security group for mlflow"

  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 5000
    to_port     = 5000
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
    Name = "my-mlflow-security-group"
  }
}

resource "aws_eip" "mlflow_elastic_ip" {
  vpc      = true
  instance = aws_instance.mlflow_instance.id
  tags = {
    Name = "mlflow_elastic_ip"
  }
}
