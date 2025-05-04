data "aws_s3_object" "lambda_zip" {
  bucket = var.lambda_artifacts_bucket_name
  key    = var.lambda_zip_key
}
