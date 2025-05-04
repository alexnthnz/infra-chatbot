resource "aws_secretsmanager_secret" "lambda_secret" {
  name = var.secret_name
}

resource "aws_secretsmanager_secret_version" "lambda_secret_version" {
  secret_id = aws_secretsmanager_secret.lambda_secret.id
  secret_string = jsonencode({
    
  })
}
