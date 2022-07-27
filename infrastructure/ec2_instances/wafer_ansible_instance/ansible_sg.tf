resource "aws_security_group" "security_group" {
  name        = var.ansible_sg_group_name
  description = "Security Group for EKS Master Server"

  ingress {
    from_port   = var.ansible_ingress_from_port
    to_port     = var.ansible_ingress_to_port
    protocol    = var.ansible_protocol
    cidr_blocks = var.ansible_cidr_block
  }

  egress {
    from_port   = var.ansible_egress_from_port
    to_port     = var.ansible_egress_to_port
    protocol    = var.ansible_protocol
    cidr_blocks = var.ansible_cidr_block
  }

  tags = {
    Name = var.ansible_sg_group_name
  }
}
