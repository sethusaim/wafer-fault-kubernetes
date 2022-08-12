resource "aws_db_instance" "mlflow" {
  identifier             = var.db_identifier
  instance_class         = var.db_instance_class
  allocated_storage      = var.db_allocated_storage
  engine                 = var.db_engine
  engine_version         = var.db_engine_version
  username               = var.db_user_name
  password               = var.db_password
  db_subnet_group_name   = aws_db_subnet_group.mlflow.name
  vpc_security_group_ids = [aws_security_group.rds.id]
  parameter_group_name   = aws_db_parameter_group.mlflow.name
  publicly_accessible    = var.db_publicly_accessible
  skip_final_snapshot    = var.db_skip_final_snaphost
}