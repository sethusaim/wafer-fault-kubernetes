resource "aws_security_group" "wafer-cluster" {
  name        = var.wafer_sg_group_name
  description = "Cluster communication with worker nodes"
  vpc_id      = aws_vpc.wafer.id

  egress {
    from_port   = var.wafer_sg_group_egress_from_port
    to_port     = var.wafer_sg_group_egress_to_port
    protocol    = var.wafer_sg_group_protocol
    cidr_blocks = var.wafer_sg_group_cidr_block
  }

  tags = {
    Name = var.wafer_sg_group_tag_name
  }
}
