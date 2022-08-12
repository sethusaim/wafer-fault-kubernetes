module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = var.aws_vpc_module_version

  name                 = var.db_vpc_name
  cidr                 = var.db_vpc_cidr
  azs                  = data.aws_availability_zones.available.names
  public_subnets       = var.db_vpc_public_subnets
  enable_dns_hostnames = var.db_vpc_enable_dns_hostname
  enable_dns_support   = var.db_vpc_enable_dns_support
}

resource "aws_db_subnet_group" "mlflow" {
  name       = var.db_subnet_group_name
  subnet_ids = module.vpc.public_subnets

  tags = {
    Name = var.db_subnet_group_tag_name
  }
}