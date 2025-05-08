module "vpc_endpoint" {
  source  = "terraform-aws-modules/vpc/aws//modules/vpc-endpoints"
  version = "5.21.0"

  vpc_id             = var.vpc_id
  subnet_ids         = var.vpc_subnet_ids
  security_group_ids = var.security_group_ids

  endpoints = {
    secretsmanager = {
      service             = "secretsmanager"
      private_dns_enabled = true
      tags = {
        Name = "secretsmanager-vpc-endpoint"
      }
    }
    bedrockruntime = {
      service             = "bedrock-runtime"
      private_dns_enabled = true
      tags = {
        Name = "bedrockruntime-vpc-endpoint"
      }
    }
  }
}
