resource "aws_s3_bucket" "raw-data" {
  bucket        = var.raw-data
  force_destroy = var.force_destroy_bucket
}