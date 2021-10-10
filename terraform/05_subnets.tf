resource "aws_subnet" "public" {
  for_each = local.network.public

  vpc_id            = aws_vpc.main.id
  cidr_block        = each.value
  availability_zone = each.key
  map_public_ip_on_launch = true

  tags = {
    Name = "revolut-public-${each.key}"
  }
}
