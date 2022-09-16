resource "aws_eks_cluster" "wafer" {
  name     = var.cluster-name
  role_arn = aws_iam_role.wafer-cluster.arn

  vpc_config {
    security_group_ids = [aws_security_group.wafer-cluster.id]
    subnet_ids         = aws_subnet.wafer[*].id
  }

  depends_on = [
    aws_iam_role_policy_attachment.wafer-cluster-AmazonEKSClusterPolicy,
    aws_iam_role_policy_attachment.wafer-cluster-AmazonEKSVPCResourceController,
  ]
}
