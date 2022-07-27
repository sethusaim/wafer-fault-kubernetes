resource "aws_security_group" "security_group" {
  name        = var.application_sg_group_name
  description = "Security Group for EKS Master Server"

  ingress {
    from_port   = var.application_ingress_from_port[0]
    to_port     = var.application_ingress_to_port[0]
    protocol    = var.application_protocol
    cidr_blocks = var.application_cidr_block
  }

  ingress {
    from_port   = var.application_ingress_from_port[1]
    to_port     = var.application_ingress_to_port[1]
    protocol    = var.application_protocol
    cidr_blocks = var.application_cidr_block
  }

  ingress {
    from_port   = var.application_ingress_from_port[2]
    to_port     = var.application_ingress_to_port[2]
    protocol    = var.application_protocol
    cidr_blocks = var.application_cidr_block
  }

  ingress {
    from_port   = var.application_ingress_from_port[3]
    to_port     = var.application_ingress_to_port[3]
    protocol    = var.application_protocol
    cidr_blocks = var.application_cidr_block
  }

  egress {
    from_port   = var.application_egress_from_port
    to_port     = var.application_egress_to_port
    protocol    = var.application_protocol
    cidr_blocks = var.application_cidr_block
  }

  tags = {
    Name = var.application_sg_group_name
  }
}