
resource "aws_iam_role" "this" {
  name = var.name
  assume_role_policy = var.trust_policy_json

  tags = {
    env = terraform.workspace
  }
}

resource "aws_iam_role_policy_attachment" "this" {
  for_each   = toset(var.policy_definition.policy_attachment)

  role       = aws_iam_role.this.name
  policy_arn = try(var.policies[each.value].arn, each.value)
}

resource "aws_iam_instance_profile" "this" {
  count   = try(var.policy_definition.create_instance_profile, false) ? 1 : 0
  name    = var.name
  role    = var.name
}