resource "aws_s3_bucket" "logs" {
  bucket        = var.logs
  force_destroy = var.force_destroy_bucket
}
