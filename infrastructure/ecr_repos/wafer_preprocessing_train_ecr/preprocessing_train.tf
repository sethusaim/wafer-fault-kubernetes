resource "aws_ecr_repository" "preprocessing_train" {
  name                 = var.wafer_preprocessing_train_ecr_name
  image_tag_mutability = var.image_tag_mutability
  force_delete         = var.force_delete_image

  image_scanning_configuration {
    scan_on_push = var.scan_on_push
  }
}