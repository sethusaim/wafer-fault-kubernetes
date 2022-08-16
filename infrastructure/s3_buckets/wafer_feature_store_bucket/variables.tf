variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "feature_store" {
  type    = string
  default = "wafer-feature-store-02126f6"
}

variable "aws_account_id" {
  type    = string
  default = "347460842118"
}

variable "force_destroy_bucket" {
  type    = bool
  default = true
}
