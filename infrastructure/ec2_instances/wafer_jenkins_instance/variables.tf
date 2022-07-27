variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "jenkins_ami" {
  type    = string
  default = "ami-0c4f7023847b90238"
}

variable "jenkins_instance_type" {
  type    = string
  default = "t2.medium"
}

variable "jenkins_key_pair_name" {
  type    = string
  default = "sethu"
}

variable "tag_name" {
  type    = string
  default = "Jenkins Server"
}

variable "jenkins_eip_name" {
  type    = string
  default = "jenkins-ip"
}

variable "jenkins_sg_group_name" {
  type    = string
  default = "jenkins_sg_group"
}

variable "jenkins_ingress_from_port" {
  type    = list(any)
  default = [22, 8080]
}

variable "jenkins_cidr_block" {
  type    = list(any)
  default = ["0.0.0.0/0"]
}

variable "jenkins_protocol" {
  type    = string
  default = "tcp"
}

variable "jenkins_ingress_to_port" {
  type    = list(any)
  default = [22, 8080]
}

variable "jenkins_egress_from_port" {
  type    = number
  default = 0
}

variable "jenkins_egress_to_port" {
  type    = number
  default = 65535
}

variable "jenkins_volume_size" {
  default = 30
  type    = number
}

variable "jenkins_volume_type" {
  default = "gp2"
  type    = string
}

variable "jenkins_volume_encryption" {
  default = true
  type    = bool
}