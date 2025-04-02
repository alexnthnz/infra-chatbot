resource "aws_s3_bucket" "model_artifacts" {
  bucket = var.model_artifacts_bucket_name
}

resource "aws_s3_bucket_versioning" "model_artifacts_versioning" {
  bucket = aws_s3_bucket.model_artifacts.id
  versioning_configuration {
    status = "Enabled"
  }
}
