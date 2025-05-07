output "lambda_security_group_arn" {
  value = module.lambda_sg.security_group_arn
}

output "lambda_security_group_id" {
  value = module.lambda_sg.security_group_id
}

output "ssm_vpc_endpoint_security_group_id" {
  value = module.vpc_endpoint_security_group.security_group_id
}
