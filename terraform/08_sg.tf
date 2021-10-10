resource "aws_security_group" "main" {
  for_each = local.sg

  name_prefix = "${each.key}_"
  description = each.value.description
  vpc_id      = aws_vpc.main.id

  tags = {
    Name = each.key
  }

  lifecycle {
    create_before_destroy = true
  }
}

module "security_group_rules" {
  source   = "./modules/sg_rules"
  for_each = local.sg

  sg_name            = each.key
  aws_security_group = aws_security_group.main
  local_sg           = local.sg

  depends_on = [aws_security_group.main]
}
