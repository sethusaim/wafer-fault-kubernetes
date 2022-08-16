resource "aws_s3_bucket" "feature_store" {
  bucket        = var.feature_store
  force_destroy = var.force_destroy_bucket
}