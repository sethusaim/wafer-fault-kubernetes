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
  default = "t2.small"

}

variable "key_pair_name" {
  type    = string
  default = "sethu"
}

variable "tag_name" {
  type    = string
  default = "MLFlow Server"
}

variable "sg_group_name" {
  type    = string
  default = "mlflow_sg_group"
}

variable "ingress_from_port" {
  type    = list(any)
  default = [22, 8080, 8000, 5000]
}

variable "ingress_to_port" {
  type    = list(any)
  default = [22, 8080, 8000, 5000]
}

variable "ingress_cidr" {
  type    = list(any)
  default = ["0.0.0.0/0"]

}

variable "protocol" {
  type    = string
  default = "tcp"
}


