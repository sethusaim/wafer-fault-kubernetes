resource "aws_s3_bucket" "train-data" {
  bucket        = var.train-data
  force_destroy = var.force_destroy_bucket
}