resource "mongodbatlas_privatelink_endpoint" "atlaspl" {
  project_id    = var.atlasprojectid
  provider_name = var.provider_name
  region        = var.aws_region
}

resource "aws_vpc" "primary" {
  cidr_block           = var.primary_vpc_cidr_block
  enable_dns_hostnames = var.enable_dns_hostnames
  enable_dns_support   = var.enable_dns_support
}

resource "aws_internet_gateway" "primary" {
  vpc_id = aws_vpc.primary.id
}

resource "aws_route" "primary-internet_access" {
  route_table_id         = aws_vpc.primary.main_route_table_id
  destination_cidr_block = var.destination_cidr_block
  gateway_id             = aws_internet_gateway.primary.id
}

resource "aws_vpc_endpoint" "ptfe_service" {
  vpc_id             = aws_vpc.primary.id
  service_name       = mongodbatlas_privatelink_endpoint.atlaspl.endpoint_service_name
  vpc_endpoint_type  = var.vpc_endpoint_type
  subnet_ids         = [aws_subnet.primary-az1.id, aws_subnet.primary-az2.id]
  security_group_ids = [aws_security_group.primary_default.id]
}

resource "mongodbatlas_privatelink_endpoint_service" "atlaseplink" {
  project_id          = mongodbatlas_privatelink_endpoint.atlaspl.project_id
  endpoint_service_id = aws_vpc_endpoint.ptfe_service.id
  private_link_id     = mongodbatlas_privatelink_endpoint.atlaspl.id
  provider_name       = var.provider_name
}