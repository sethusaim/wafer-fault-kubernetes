variable "wafer_load_prod_model_ecr_name" {
  default = "wafer_load_prod_model"
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