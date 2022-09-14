variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "mlflow_ami" {
  type    = string
  default = "ami-0c4f7023847b90238"
}

variable "mlflow_instance_type" {
  type    = string
  default = "t2.small"
}

variable "mlflow_key_pair_name" {
  type    = string
  default = "sethusaim"
}

variable "mlflow_tag_name" {
  type    = string
  default = "MLFlow Server"
}

variable "mlflow_eip_name" {
  type    = string
  default = "MLFlow_Elastic_IP"
}

variable "mlflow_sg_group_name" {
  type    = string
  default = "mlflow_sg_group"
}

variable "mlflow_ingress_from_port" {
  type    = list(number)
  default = [22, 8080, 8000, 5000, 9090, 9100]
}

variable "mlflow_ingress_to_port" {
  type    = list(number)
  default = [22, 8080, 8000, 5000, 9090, 9100]
}

variable "mlflow_cidr_block" {
  type    = list(string)
  default = ["0.0.0.0/0"]
}

variable "mlflow_protocol" {
  type    = string
  default = "tcp"
}

variable "mlflow_egress_from_port" {
  type    = number
  default = 0
}

variable "mlflow_egress_to_port" {
  type    = number
  default = 65535
}

variable "mlflow_volume_size" {
  default = 30
  type    = number
}

variable "mlflow_volume_type" {
  default = "gp2"
  type    = string
}

variable "mlflow_volume_encryption" {
  default = true
  type    = bool
}