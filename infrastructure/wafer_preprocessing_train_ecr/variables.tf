variable "wafer_preprocessing_train_ecr_name" {
  default = "wafer_preprocessing_train"
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