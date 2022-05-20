variable "atlasprojectid" {
  default = "628778847503c36560b75ddf"
  type    = string
}

variable "atlas_region" {
  default = "US_EAST_1"
  type    = string
}

variable "aws_region" {
  default = "us-east-1"
  type    = string
}

variable "database_name" {
  default = "wafer-db"
  type    = string
}

variable "mongo_version" {
  default = "4.2"
  type    = string
}

variable "cloud_backup" {
  default = true
  type    = bool
}

variable "auto_scaling_disk_gb_enabled" {
  default = true
  type    = bool
}

variable "cluster_type" {
  default = "REPLICASET"
  type    = string
}

variable "num_shards" {
  default = 1
  type    = number
}

variable "electable_nodes" {
  default = 3
  type    = number
}

variable "priority" {
  default = 7
  type    = number
}

variable "read_only_nodes" {
  default = 0
  type    = number
}

variable "provider_name" {
  default = "AWS"
  type    = string
}

variable "disk_size_gb" {
  default = 10
  type    = number
}

variable "provider_instance_size_name" {
  default = "M10"
  type    = string
}

variable "vpc_endpoint_type" {
  default = "Interface"
  type    = string
}

variable "primary_vpc_cidr_block" {
  default = "10.0.0.0/16"
  type    = string
}

variable "enable_dns_hostnames" {
  default = true
  type    = bool
}

variable "enable_dns_support" {
  default = true
  type    = bool
}

variable "destination_cidr_block" {
  default = "0.0.0.0/0"
  type    = string
}

variable "primary_subnet_az1" {
  default = "10.0.1.0/24"
  type    = string
}

variable "primary_subnet_az2" {
  default = "10.0.2.0/24"
  type    = string
}

variable "sg_group_protocol" {
  default = "tcp"
  type    = string
}

variable "sg_group_from_port" {
  default = 0
  type    = number
}

variable "sg_group_to_port" {
  default = 0
  type    = number
}

variable "sg_group_cidr_block" {
  default = ["0.0.0.0/0"]
  type    = list(string)
}

variable "sg_group_egress_from_port" {
  default = 0
  type    = number
}

variable "sg_group_egress_to_port" {
  default = 0
  type    = number
}

variable "sg_group_egress_protocol" {
  default = "-1"
  type    = string
}

variable "sg_group_egress_cidr_block" {
  default = ["0.0.0.0/0"]
  type    = list(string)
}

