resource "aws_secretsmanager_secret" "lambda_secret" {
  name = var.secret_name
}
