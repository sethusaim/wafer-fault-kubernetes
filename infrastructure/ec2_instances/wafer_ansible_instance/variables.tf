variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "ansible_ami" {
  type    = string
  default = "ami-0c4f7023847b90238"
}

variable "ansible_instance_type" {
  type    = string
  default = "t2.medium"
}

variable "ansible_key_pair_name" {
  type    = string
  default = "sethusaim"
}

variable "ansible_tag_name" {
  type    = string
  default = "Ansible Server"
}

variable "ansible_eip_name" {
  type    = string
  default = "ansible_ip"
}

variable "ansible_sg_group_name" {
  type    = string
  default = "ansible_sg_group"
}

variable "ansible_ingress_from_port" {
  type    = list(number)
  default = [22, 9100, 9090]
}

variable "ansible_cidr_block" {
  type    = list(string)
  default = ["0.0.0.0/0"]
}

variable "ansible_protocol" {
  type    = string
  default = "tcp"
}

variable "ansible_ingress_to_port" {
  type    = list(number)
  default = [22, 9100, 9090]
}

variable "ansible_egress_from_port" {
  type    = number
  default = 0
}

variable "ansible_egress_to_port" {
  type    = number
  default = 65535
}

variable "ansible_volume_size" {
  default = 30
  type    = number
}

variable "ansible_volume_type" {
  default = "gp2"
  type    = string
}

variable "ansible_volume_encryption" {
  default = true
  type    = bool
}