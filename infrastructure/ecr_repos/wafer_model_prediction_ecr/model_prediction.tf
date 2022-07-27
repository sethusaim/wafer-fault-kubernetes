resource "aws_ecr_repository" "model_prediction" {
  name                 = var.wafer_model_prediction_ecr_name
  image_tag_mutability = var.image_tag_mutability

  image_scanning_configuration {
    scan_on_push = var.scan_on_push
  }
}