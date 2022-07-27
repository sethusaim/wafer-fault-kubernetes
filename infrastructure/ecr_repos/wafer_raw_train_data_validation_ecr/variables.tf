variable "wafer_raw_train_data_validation_ecr_name" {
  default = "wafer_raw_train_data_validation"
  type    = string
}

variable "image_tag_mutability" {
  default = "MUTABLE"
  type    = string
}

variable "scan_on_push" {
  default = true
  type    = bool
}