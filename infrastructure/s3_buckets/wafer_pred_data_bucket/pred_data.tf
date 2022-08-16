resource "aws_s3_bucket" "pred-data" {
  bucket        = var.pred-data
  force_destroy = var.force_destroy_bucket
}
