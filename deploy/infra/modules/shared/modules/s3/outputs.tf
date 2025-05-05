output "s3_bucket_name" {
  description = "Name of the S3 bucket for file storage"
  value       = aws_s3_bucket.file_bucket.bucket
}

output "s3_bucket_arn" {
  description = "Amazon Resource Name (ARN) of the S3 bucket"
  value       = aws_s3_bucket.file_bucket.arn
}
