resource "aws_s3_bucket" "example" {
  bucket = "my-tf-test-bucket-sethu"
}

resource "aws_s3_bucket_policy" "allow_full_access" {
  bucket = aws_s3_bucket.example.id
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
