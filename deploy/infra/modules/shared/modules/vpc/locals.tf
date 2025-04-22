locals {
  private_subnets = [
    cidrsubnet(var.cidr_block, 8, 1),
    cidrsubnet(var.cidr_block, 8, 2),
  ]
  public_subnets = [
    cidrsubnet(var.cidr_block, 8, 3),
    cidrsubnet(var.cidr_block, 8, 4),
  ]
  database_subnets = [
    cidrsubnet(var.cidr_block, 8, 5),
    cidrsubnet(var.cidr_block, 8, 6),
  ]
  intra_subnets = [
    cidrsubnet(var.cidr_block, 8, 7),
    cidrsubnet(var.cidr_block, 8, 8),
  ]
}
