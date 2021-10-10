
resource "aws_security_group_rule" "ingress_sg" {
  for_each = { for rule in try(var.local_sg[var.sg_name].ingress_rules_sg, []) : rule.description => rule }

  type                     = "ingress"
  description              = each.value.description
  from_port                = each.value.from_port
  to_port                  = each.value.to_port
  protocol                 = each.value.protocol
  source_security_group_id = try(var.aws_security_group[each.value.source_security_group].id, "ID for ${each.value.source_security_group} not found")
  security_group_id        = var.aws_security_group[var.sg_name].id
}

resource "aws_security_group_rule" "ingress_cidr" {
  for_each = { for rule in try(var.local_sg[var.sg_name].ingress_rules_cidr, []) : rule.description => rule }

  type                     = "ingress"
  description              = each.value.description
  from_port                = each.value.from_port
  to_port                  = each.value.to_port
  protocol                 = each.value.protocol
  cidr_blocks              = each.value.cidr_blocks
  security_group_id        = var.aws_security_group[var.sg_name].id
}