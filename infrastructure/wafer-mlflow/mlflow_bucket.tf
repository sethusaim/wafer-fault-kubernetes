resource "aws_s3_bucket" "mlflow" {
    bucket = var.mlflow
  
}

resource "aws_s3_bucket_policy" "allow_full_access" {
  bucket = aws_s3_bucket.mlflow.id
  policy = data.aws_iam_policy_document.allow_full_access.json
}


data "aws_iam_policy_document" "allow_full_access" {
  statement {
    principals {
      type        = "AWS"
      identifiers = [var.aws_account_id]
    }

    actions = ["s3:*"]

    resources = [
      aws_s3_bucket.logs.arn,
      "${aws_s3_bucket.logs.arn}/*",
    ]
  }
}
