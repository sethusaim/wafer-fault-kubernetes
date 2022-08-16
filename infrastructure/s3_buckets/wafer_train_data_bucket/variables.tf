variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "train-data" {
  type    = string
  default = "wafer-train-data-5acbd2d"
}

variable "aws_account_id" {
  type    = string
  default = "347460842118"
}

variable "force_destroy_bucket" {
  type    = bool
  default = true
}
