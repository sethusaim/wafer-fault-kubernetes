variable "aws_region" {
  type    = string
  default = "us-east-1"

}

variable "ami" {
  type    = string
  default = "ami-0022f774911c1d690"
}

variable "instance_type" {
  type    = string
  default = "t2.medium"

}

variable "key_pair_name" {
  type    = string
  default = "sethu"
}

variable "tag_name" {
  type    = string
  default = "Jenkins Server"
}

variable "sg_group_name" {
  type    = string
  default = "jenkins_sg_group"
}

variable "ingress_from_port" {
  type    = list(any)
  default = [22, 8080]
}

variable "ingress_cidr" {
  type    = list(any)
  default = ["0.0.0.0/0"]

}

variable "protocol" {
  type    = string
  default = "tcp"
}

variable "ingress_to_port" {
  type    = list(any)
  default = [22, 8080]
}
