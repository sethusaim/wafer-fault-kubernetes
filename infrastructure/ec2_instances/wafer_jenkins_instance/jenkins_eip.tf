resource "aws_eip" "elastic_ip" {
  vpc      = true
  instance = aws_instance.jenkins_instance.id
  tags = {
    Name = var.jenkins_eip_name
  }
}