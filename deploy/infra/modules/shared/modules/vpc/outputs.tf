output "vpc_id" {
  description = "The ID of the VPC."
  value       = module.vpc.default_vpc_id
}
