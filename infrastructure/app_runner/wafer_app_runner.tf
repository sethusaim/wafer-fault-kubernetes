resource "aws_apprunner_service" "search_data_collection_apprunner_service" {
  service_name = var.app_runner_service_name
  source_configuration {
    authentication_configuration {
      access_role_arn = aws_iam_role.apprunner-service-role.arn
    }
    image_repository {
      image_configuration {
        port = var.app_runner_service_port
      }
      image_identifier      = var.app_runner_service_image_url
      image_repository_type = var.app_runner_service_image_repository_type
    }
    auto_deployments_enabled = var.app_runner_service_auto_deployments_enabled
  }
  instance_configuration {
    cpu = var.app_runner_service_cpu
    memory = var.app_runner_service_memory
  }
}