resource "aws_security_group" "primary_default" {
  name_prefix = "default-"
  description = "Default security group for all instances in ${aws_vpc.primary.id}"
  vpc_id      = aws_vpc.primary.id
  ingress {
    from_port   = var.sg_group_from_port
    to_port     = var.sg_group_to_port
    protocol    = var.sg_group_protocol
    cidr_blocks = var.sg_group_cidr_block
  }
  egress {
    from_port   = var.sg_group_egress_from_port
    to_port     = var.sg_group_egress_to_port
    protocol    = var.sg_group_egress_protocol
    cidr_blocks = var.sg_group_egress_cidr_block
  }
}