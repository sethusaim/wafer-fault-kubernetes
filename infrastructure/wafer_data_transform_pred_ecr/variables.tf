variable "wafer_data_transform_pred_ecr_name" {
  default = "wafer_data_transform_pred"
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