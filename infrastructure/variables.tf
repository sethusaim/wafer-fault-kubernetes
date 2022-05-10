variable "aws_region" {
  default = "us-east-1"
}

variable "wafer_cluster_name" {
  default = "terraform-eks-demo"
  type    = string
}

variable "wafer_cluster_iam_role_name" {
  default = "terraform-eks-wafer-cluster"
  type    = string
}

variable "wafer_cluster_sg_group_name" {
  default = "terraform_eks_wafer_cluster_sg_group"
  type    = string
}

variable "cluster_ingress_from_port" {
  default = 443
  type    = number
}

variable "cluster_ingress_to_port" {
  default = 443
  type    = number
}

variable "cluster_protocol" {
  default = "tcp"
  type    = string
}

variable "cluster_cidr_block" {
  default = ["0.0.0.0/0"]
  type    = list(string)
}

variable "cluster_egress_from_port" {
  default = 0
  type    = number
}

variable "cluster_egress_to_port" {
  default = 0
  type    = number
}

variable "cluster_sg_group_name" {
  default = "terraform_eks_wafer_sg_group"
  type    = string
}

variable "cluster_node_iam_role_name" {
  default = "terraform_eks_wafer_node"
  type    = string
}

variable "cluster_node_group_name" {
  default = "wafer"
  type    = string
}

variable "max_nodes_size" {
  default = 3
  type    = number
}

variable "min_nodes_size" {
  default = 1
  type    = number
}

variable "required_nodes_size" {
  default = 2
  type    = number
}


variable "cluster_vpc_cidr_block" {
  default = "10.0.0.0/16"
  type    = string
}

variable "cluster_vpc_node_group_name" {
  default = "terraform-eks-wafer-node"
  type    = string
}

variable "cluster_internet_gateway_tag" {
  default = "terraform-eks-wafer"
  type    = string
}

