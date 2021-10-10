resource "aws_db_subnet_group" "main" {
  name       = "revolut-private"
  subnet_ids = [ for subnet in aws_subnet.public: subnet.id]

  tags = {
    Name = "Private db subnet group for revolut challenge"
  }
}

resource "aws_db_instance" "db" {
  for_each = local.rds

  allocated_storage            = each.value.allocated_storage
  engine                       = each.value.engine
  engine_version               = each.value.engine_version
  instance_class               = each.value.instance_class
  name                         = each.value.db_name
  identifier                   = each.key
  port                         = each.value.port
  username                     = "revolut"
  password                     = var.rds_password
  availability_zone            = each.value.availability_zone
  backup_retention_period      = each.value.backup_retention_period
  db_subnet_group_name         = aws_db_subnet_group.main.name
  storage_encrypted            = true
  performance_insights_enabled = each.value.performance_insights_enabled
  monitoring_interval          = each.value.monitoring_interval
  vpc_security_group_ids       = [for sg in each.value.db_security_groups : aws_security_group.main[sg].id]
  skip_final_snapshot          = true
}
