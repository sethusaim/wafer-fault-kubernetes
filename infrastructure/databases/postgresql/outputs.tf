output "rds_hostname" {
  value = aws_db_instance.mlflow.address
}

output "rds_port" {
  value = aws_db_instance.mlflow.port
}

output "rds_username" {
  value = aws_db_instance.mlflow.username
}