resource "aws_db_parameter_group" "mlflow" {
  name   = var.db_parameter_group_name
  family = var.db_parameter_group_family

  parameter {
    name  = var.db_parameter_group_parameter_name
    value = var.db_parameter_group_parameter_value
  }
}