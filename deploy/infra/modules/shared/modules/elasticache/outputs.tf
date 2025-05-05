output "elasticache_arn" {
  description = "The amazon resource name of the serverless cache"
  value       = aws_elasticache_serverless_cache.redis_serverless_cache.arn
}

output "elasticache_endpoint" {
  description = "The endpoint of the serverless cache"
  value       = aws_elasticache_serverless_cache.redis_serverless_cache.endpoint
}

output "elasticache_security_group_id" {
  description = "The security group ID of the serverless cache"
  value       = module.security_group_redis.security_group_id
}
