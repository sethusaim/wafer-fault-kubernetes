variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "artifacts_bucket_name" {
  type    = string
  default = "truck-feature-store"
}

variable "aws_account_id" {
  type    = string
  default = "347460842118"
}

variable "force_destroy_bucket" {
  type    = bool
  default = true
}