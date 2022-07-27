resource "aws_eip" "elastic_ip" {
  vpc      = true
  instance = aws_instance.ansible_instance.id
  tags = {
    Name = var.ansible_eip_name
  }
}