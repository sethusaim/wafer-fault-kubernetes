resource "aws_ecr_repository" "load_prod_model" {
  name                 = var.wafer_load_prod_model_ecr_name
  image_tag_mutability = var.image_tag_mutability
  force_delete         = var.force_delete_image

  image_scanning_configuration {
    scan_on_push = var.scan_on_push
  }
}