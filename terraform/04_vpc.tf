resource "aws_vpc" "main" {
  cidr_block = local.network.vpc.cidr

  enable_dns_support   = "true"
  enable_dns_hostnames = "true"

  tags = {
    Name = "revolut"
  }
}
