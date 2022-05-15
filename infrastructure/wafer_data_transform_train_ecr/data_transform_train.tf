resource "aws_ecr_repository" "data_transform_train" {
  name                 = var.wafer_data_transform_train_ecr_name
  image_tag_mutability = var.image_tag_mutability

  image_scanning_configuration {
    scan_on_push = var.scan_on_push
  }
}


