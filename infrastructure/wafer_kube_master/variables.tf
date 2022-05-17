variable "aws_region" {
  type    = string
  default = "us-east-1"

}

variable "eks_master_ami" {
  type    = string
  default = "ami-0c4f7023847b90238"
}

variable "eks_master_instance_type" {
  type    = string
  default = "t2.micro"

}

variable "eks_master_key_pair_name" {
  type    = string
  default = "sethu"
}

variable "eks_master_tag_name" {
  type    = string
  default = "EKS Master Server"
}

variable "eks_master_eip_name" {
  type    = string
  default = "eks_master_ip"

}

variable "eks_master_sg_group_name" {
  type    = string
  default = "eks_master_sg_group"
}

variable "eks_master_ingress_from_port" {
  type    = list(number)
  default = [22, 8080]
}

variable "eks_master_cidr_block" {
  type    = list(string)
  default = ["0.0.0.0/0"]

}

variable "eks_master_protocol" {
  type    = string
  default = "tcp"
}

variable "eks_master_ingress_to_port" {
  type    = list(number)
  default = [22, 8080]
}

variable "eks_master_egress_from_port" {
  type    = number
  default = 0
}

variable "eks_master_egress_to_port" {
  type    = number
  default = 65535
}

variable "eks_master_volume_size" {
  default = 30
  type    = number
}

variable "eks_master_volume_type" {
  default = "gp2"
  type    = string
}

variable "eks_master_volume_encryption" {
  default = true
  type    = bool
}