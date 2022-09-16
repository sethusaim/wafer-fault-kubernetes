resource "aws_route_table" "wafer" {
  vpc_id = aws_vpc.wafer.id

  route {
    cidr_block = var.route_table_cidr_block
    gateway_id = aws_internet_gateway.wafer.id
  }
}

resource "aws_route_table_association" "wafer" {
  count = 2

  subnet_id      = aws_subnet.wafer.*.id[count.index]
  route_table_id = aws_route_table.wafer.id
}