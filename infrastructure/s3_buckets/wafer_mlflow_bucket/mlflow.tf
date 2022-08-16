resource "aws_s3_bucket" "mlflow" {
  bucket        = var.mlflow
  force_destroy = var.force_destroy_bucket
}
