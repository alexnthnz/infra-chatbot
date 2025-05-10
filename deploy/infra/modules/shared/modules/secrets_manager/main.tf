resource "aws_secretsmanager_secret" "lambda_secret" {
  name = var.secret_name

  recovery_window_in_days = 0
}

resource "aws_secretsmanager_secret_version" "lambda_secret_version" {
  secret_id = aws_secretsmanager_secret.lambda_secret.id

  # Initialize secret with JSON containing four environment variables
  secret_string = jsonencode({
    DATABASE_URL         = ""
    AWS_REGION_NAME      = ""
    AWS_BEDROCK_MODEL_ID = ""
    SERPER_API_KEY       = ""
  })

  # Ensure the secret is created before setting the version
  depends_on = [aws_secretsmanager_secret.lambda_secret]
}
