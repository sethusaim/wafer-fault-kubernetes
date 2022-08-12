variable "region" {
  default     = "us-east-2"
  description = "AWS region"
}

variable "db_user_name" {
  default = "username"
  type    = string
}

variable "db_password" {
  default = "password"
  type    = string
}

variable "db_engine_version" {
  default = "14"
  type    = string
}

variable "db_engine" {
  default = "postgres"
  type    = string
}

variable "db_allocated_storage" {
  default = 5
  type    = number
}

variable "db_instance_class" {
  default = "db.t3.micro"
  type    = string
}

variable "db_identifier" {
  default = "mlflow_db_instance"
  type    = string
}

variable "db_publicly_accessible" {
  default = true
  type    = bool
}

variable "db_skip_final_snaphost" {
  default = true
  type    = true
}

variable "db_sg_name" {
  default = "mlflow_rds_sg"
  type    = string
}

variable "db_ingress_from_port" {
  default = 5432
  type    = number
}

variable "db_ingress_to_port" {
  default = 5432
  type    = number
}

variable "db_ingress_protocol" {
  default = "tcp"
  type    = string
}

variable "db_ingress_cidr_blocks" {
  default = ["0.0.0.0/0"]
  type    = list(string)
}

variable "db_egress_from_port" {
  default = 5432
  type    = number
}

variable "db_egress_to_port" {
  default = 5432
  type    = number
}

variable "db_egress_protocol" {
  default = "tcp"
  type    = string
}

variable "db_egress_cidr_blocks" {
  default = ["0.0.0.0/0"]
  type    = string
}

variable "db_sg_tag_name" {
  default = "mlflow_rds"
  type    = string
}

variable "aws_vpc_module_version" {
  default = "3.14.2"
  type    = string
}

variable "db_vpc_name" {
  default = "mlflow_rds"
  type    = string
}

variable "db_vpc_cidr" {
  default = "10.0.0.0/16"
  type    = string
}

variable "db_vpc_public_subnets" {
  default = ["10.0.4.0/24", "10.0.5.0/24", "10.0.6.0/24"]
  type    = list(string)
}

variable "db_vpc_enable_dns_hostname" {
  default = true
  type    = bool
}

variable "db_vpc_enable_dns_support" {
  default = true
  type    = bool
}

variable "db_subnet_group_name" {
  default = "mlflow_subnet"
  type    = string
}

variable "db_subnet_group_tag_name" {
  default = "MLFlow RDS"
  type    = string
}

variable "db_parameter_group_name" {
  default = "mlflow_rds_pg"
  type    = string
}

variable "db_parameter_group_family" {
  default = "postgres14"
  type    = string
}

variable "db_parameter_group_parameter_name" {
  default = "log_connections"
  type    = string
}

variable "db_parameter_group_parameter_value" {
  default = "1"
  type    = string
}