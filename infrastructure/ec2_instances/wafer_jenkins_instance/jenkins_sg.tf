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