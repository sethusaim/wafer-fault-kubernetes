resource "aws_ecr_repository" "raw_train_data_validation" {
  name                 = var.wafer_raw_train_data_validation_ecr_name
  force_delete         = var.force_delete_image
  image_tag_mutability = var.image_tag_mutability

  image_scanning_configuration {
    scan_on_push = var.scan_on_push
  }
}
