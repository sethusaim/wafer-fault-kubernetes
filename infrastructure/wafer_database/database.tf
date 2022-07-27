terraform {
  required_providers {
    mongodbatlas = {
      source = "mongodb/mongodbatlas"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

resource "mongodbatlas_cluster" "cluster-atlas" {
  project_id                   = var.atlasprojectid
  name                         = var.database_name
  cloud_backup                 = var.auto_scaling_disk_gb_enabled
  auto_scaling_disk_gb_enabled = var.cloud_backup
  mongo_db_major_version       = var.mongo_version
  cluster_type                 = var.cluster_type
  replication_specs {
    num_shards = var.num_shards
    regions_config {
      region_name     = var.atlas_region
      electable_nodes = var.electable_nodes
      priority        = var.priority
      read_only_nodes = var.read_only_nodes
    }
  }

  provider_name               = var.provider_name
  disk_size_gb                = var.disk_size_gb
  provider_instance_size_name = var.provider_instance_size_name
}

data "mongodbatlas_cluster" "cluster-atlas" {
  project_id = var.atlasprojectid
  name       = mongodbatlas_cluster.cluster-atlas.name
  depends_on = [mongodbatlas_privatelink_endpoint_service.atlaseplink]
}


resource "mongodbatlas_privatelink_endpoint" "atlaspl" {
  project_id    = var.atlasprojectid
  provider_name = var.provider_name
  region        = var.aws_region
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

output "atlasclusterstring" {
  value = data.mongodbatlas_cluster.cluster-atlas.connection_strings
}

output "plstring" {
  value = lookup(data.mongodbatlas_cluster.cluster-atlas.connection_strings[0].aws_private_link_srv, aws_vpc_endpoint.ptfe_service.id)
}
