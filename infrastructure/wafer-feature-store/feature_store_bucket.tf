

resource "aws_s3_bucket" "feature_store" {
  bucket = "wafer-feature-store-02126f6"
}

resource "aws_s3_bucket_policy" "allow_full_access" {
  bucket = aws_s3_bucket.feature_store.id
  policy = data.aws_iam_policy_document.allow_full_access.json
}


data "aws_iam_policy_document" "allow_full_access" {
  statement {
    principals {
      type        = "AWS"
      identifiers = ["347460842118"]
    }

    actions = ["s3:*"]

    resources = [
      aws_s3_bucket.example.arn,
      "${aws_s3_bucket.example.arn}/*",
    ]
  }
}
