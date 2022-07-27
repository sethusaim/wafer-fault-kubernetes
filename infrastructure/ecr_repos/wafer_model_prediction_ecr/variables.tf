variable "wafer_model_prediction_ecr_name" {
  default = "wafer_model_prediction"
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