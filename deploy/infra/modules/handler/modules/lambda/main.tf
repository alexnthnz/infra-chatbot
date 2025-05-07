resource "aws_lambda_layer_version" "app_layer" {
  layer_name               = "${var.lambda_function_name}-layer"
  s3_bucket                = var.lambda_s3_bucket_name
  s3_key                   = var.lambda_layer_zip_key
  compatible_architectures = ["x86_64"]
  compatible_runtimes      = ["python3.13"]

  source_code_hash = data.aws_s3_object.lambda_layer_zip.etag
}

resource "aws_lambda_function" "app" {
  s3_bucket     = var.lambda_s3_bucket_name
  s3_key        = var.lambda_zip_key # e.g., "lambda-deployment.zip"
  function_name = var.lambda_function_name
  role          = var.lambda_role_arn
  handler       = "src.lambda_handler.handler"
  runtime       = "python3.13"
  timeout       = 60
  memory_size   = 512

  layers = [
    aws_lambda_layer_version.app_layer.arn,
  ]

  # Add source_code_hash to detect S3 object changes
  source_code_hash = data.aws_s3_object.lambda_zip.etag

  environment {
    variables = {
      SECRET_ARN = var.secret_arn
    }
  }

  vpc_config {
    subnet_ids         = var.subnet_ids
    security_group_ids = [var.lambda_security_group_id]
  }
}
