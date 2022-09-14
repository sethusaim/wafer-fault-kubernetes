resource "aws_ecr_repository" "mlflow" {
  name                 = var.wafer_mlflow_ecr_name
  image_tag_mutability = var.image_tag_mutability
  force_delete         = var.force_delete_image

  image_scanning_configuration {
    scan_on_push = var.scan_on_push
  }
}