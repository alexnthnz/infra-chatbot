resource "aws_lambda_function" "app" {
  image_uri     = var.lambda_function_ecr_image_uri
  function_name = var.lambda_function_name
  role          = var.lambda_role_arn
  timeout       = 60
  memory_size   = 512
  package_type  = "Image"

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
