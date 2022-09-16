resource "aws_eks_node_group" "wafer" {
  cluster_name    = aws_eks_cluster.wafer.name
  node_group_name = var.eks_node_group_name
  node_role_arn   = aws_iam_role.wafer-node.arn
  instance_types  = [var.clutser_instance_type]
  subnet_ids      = aws_subnet.wafer[*].id

  scaling_config {
    desired_size = var.desired_node_size
    max_size     = var.max_node_size
    min_size     = var.min_node_size
  }

  depends_on = [
    aws_iam_role_policy_attachment.wafer-node-AmazonEKSWorkerNodePolicy,
    aws_iam_role_policy_attachment.wafer-node-AmazonEKS_CNI_Policy,
    aws_iam_role_policy_attachment.wafer-node-AmazonEC2ContainerRegistryReadOnly,
  ]
}
