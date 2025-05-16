resource "aws_apigatewayv2_api" "http_api" {
  name                       = var.api_gateway_name
  protocol_type              = "HTTP"
  route_selection_expression = "$request.method $request.path"

  cors_configuration {
    allow_origins = ["*"] # Adjust to specific origins in production
    allow_methods = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    allow_headers = ["Content-Type", "Authorization"]
    max_age       = 300
  }
}

resource "aws_lambda_permission" "api_gateway" {
  statement_id  = "AllowInvokeFromAPIGW"
  action        = "lambda:InvokeFunction"
  function_name = var.lambda_function_name
  principal     = "apigateway.amazonaws.com"
  # Lock it down to your stage:
  source_arn = "${aws_apigatewayv2_api.http_api.execution_arn}/*/*"
}

resource "aws_apigatewayv2_integration" "proxy" {
  api_id                 = aws_apigatewayv2_api.http_api.id
  integration_type       = "AWS_PROXY"
  integration_uri        = var.lambda_function_invoke_arn
  integration_method     = "POST"
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "default" {
  api_id    = aws_apigatewayv2_api.http_api.id
  route_key = "$default"
  target    = "integrations/${aws_apigatewayv2_integration.proxy.id}"
}

resource "aws_cloudwatch_log_group" "api_gw" {
  name              = "/aws/http-api/${aws_apigatewayv2_api.http_api.name}"
  retention_in_days = 7
}

resource "aws_apigatewayv2_stage" "default" {
  api_id      = aws_apigatewayv2_api.http_api.id
  name        = "$default"
  auto_deploy = true

  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.api_gw.arn
    format = jsonencode({
      requestId               = "$context.requestId"
      routeKey                = "$context.routeKey"
      status                  = "$context.status"
      responseLatency         = "$context.responseLatency"
      integrationErrorMessage = "$context.integrationErrorMessage"
    })
  }

  default_route_settings {
    logging_level          = "INFO"
    data_trace_enabled     = true
    throttling_burst_limit = 2000
    throttling_rate_limit  = 1000
  }
}
