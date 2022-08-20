resource "aws_ecr_repository" "db_operation_pred" {
  name                 = var.wafer_db_operation_pred_ecr_name
  image_tag_mutability = var.image_tag_mutability
  force_delete         = var.force_delete_image

  image_scanning_configuration {
    scan_on_push = var.scan_on_push
  }
}