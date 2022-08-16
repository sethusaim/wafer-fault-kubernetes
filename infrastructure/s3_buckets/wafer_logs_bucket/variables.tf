variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "logs" {
  type    = string
  default = "wafer-logs-4e1f3bd"
}

variable "aws_account_id" {
  type    = string
  default = "347460842118"
}

variable "force_destroy_bucket" {
  type    = bool
  default = true
}
