variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "ami" {
  type    = string
  default = "ami-0c4f7023847b90238"
}

variable "instance_type" {
  type    = string
  default = "t2.micro"

}

variable "key_pair_name" {
  type    = string
  default = "sethu"
}

variable "tag_name" {
  type    = string
  default = "Kube Master"
}

variable "sg_group_name" {
  type    = string
  default = "mlflow_sg_group"
}

variable "ingress_from_port" {
  type    = number
  default = 22
}

variable "ingress_to_port" {
  type    = list(any)
  default = 22
}

variable "egress_from_port" {
  type    = number
  default = 0
}

variable "egress_to_port" {
  type    = number
  default = 65535
}

variable "cidr_block" {
  type    = list(any)
  default = ["0.0.0.0/0"]

}

variable "protocol" {
  type    = string
  default = "tcp"
}


