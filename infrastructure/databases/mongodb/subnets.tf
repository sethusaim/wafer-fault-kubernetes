resource "aws_subnet" "primary-az1" {
  vpc_id                  = aws_vpc.primary.id
  cidr_block              = var.primary_subnet_az1
  map_public_ip_on_launch = true
  availability_zone       = "${var.aws_region}a"
}

resource "aws_subnet" "primary-az2" {
  vpc_id                  = aws_vpc.primary.id
  cidr_block              = var.primary_subnet_az2
  map_public_ip_on_launch = false
  availability_zone       = "${var.aws_region}b"
}