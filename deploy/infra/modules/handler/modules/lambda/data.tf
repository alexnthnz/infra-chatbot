data "aws_s3_object" "lambda_zip" {
  bucket = var.lambda_s3_bucket_name
  key    = var.lambda_zip_key
}
