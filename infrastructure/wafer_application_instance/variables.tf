variable "aws_region" {
  type    = string
  default = "us-east-1"

}

variable "application_ami" {
  type    = string
  default = "ami-0c4f7023847b90238"
}

variable "application_instance_type" {
  type    = string
  default = "t2.medium"

}

variable "application_key_pair_name" {
  type    = string
  default = "sethu"
}

variable "application_tag_name" {
  type    = string
  default = "Application Server"
}

variable "application_eip_name" {
  type    = string
  default = "application_ip"

}

variable "application_sg_group_name" {
  type    = string
  default = "application_sg_group"
}

variable "application_ingress_from_port" {
  type    = list(number)
  default = [22, 8080, 80.8000]
}

variable "application_cidr_block" {
  type    = list(string)
  default = ["0.0.0.0/0"]

}

variable "application_protocol" {
  type    = string
  default = "tcp"
}

variable "application_ingress_to_port" {
  type    = list(number)
  default = [22, 8080, 80, 8000]
}

variable "application_egress_from_port" {
  type    = number
  default = 0
}

variable "application_egress_to_port" {
  type    = number
  default = 65535
}

variable "application_volume_size" {
  default = 30
  type    = number
}

variable "application_volume_type" {
  default = "gp2"
  type    = string
}

variable "application_volume_encryption" {
  default = true
  type    = bool
}
