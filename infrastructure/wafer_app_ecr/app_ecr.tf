resource "aws_ecr_repository" "app_ecr_repo" {
  name                 = var.wafer_app_ecr_name
  image_tag_mutability = var.image_tag_mutability

  image_scanning_configuration {
    scan_on_push = var.scan_on_push
  }
}