variable "app_runner_service_name" {
  default = "search_data_collection_apprunner_service"
  type    = string
}

variable "app_runner_service_port" {
  default = 8080
  type    = number
}

variable "app_runner_service_image_url" {
  default = "347460842118.dkr.ecr.us-east-1.amazonaws.com/wafer_mlflow:latest"
  type    = string
}

variable "app_runner_service_image_repository_type" {
  default = "ECR"
  type    = string
}

variable "app_runner_service_auto_deployments_enabled" {
  default = true
  type    = bool
}

variable "app_runner_service_role_name" {
  default = "apprunner_service_role"
  type    = string
}

variable "app_runner_service_cpu" {
  default = 1024
  type = number
}

variable "app_runner_service_memory" {
  default = 2048
  type = number
}