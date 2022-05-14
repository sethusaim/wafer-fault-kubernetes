resource "aws_iam_role" "wafer-cluster" {
  name = "terraform-eks-wafer-cluster"

  assume_role_policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "eks.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
POLICY
}

resource "aws_iam_role_policy_attachment" "wafer-cluster-AmazonEKSClusterPolicy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
  role       = aws_iam_role.wafer-cluster.name
}

resource "aws_iam_role_policy_attachment" "wafer-cluster-AmazonEKSVPCResourceController" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSVPCResourceController"
  role       = aws_iam_role.wafer-cluster.name
}

resource "aws_security_group" "wafer-cluster" {
  name        = var.wafer_sg_group_name
  description = "Cluster communication with worker nodes"
  vpc_id      = aws_vpc.wafer.id

  egress {
    from_port   = var.wafer_sg_group_egress_from_port
    to_port     = var.wafer_sg_group_egress_to_port
    protocol    = var.wafer_sg_group_protocol
    cidr_blocks = var.wafer_sg_group_cidr_block
  }

  tags = {
    Name = var.wafer_sg_group_tag_name
  }
}

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

resource "aws_iam_role" "wafer-node" {
  name = var.wafer_node_iam_role_name

  assume_role_policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
POLICY
}

resource "aws_iam_role_policy_attachment" "wafer-node-AmazonEKSWorkerNodePolicy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
  role       = aws_iam_role.wafer-node.name
}

resource "aws_iam_role_policy_attachment" "wafer-node-AmazonEKS_CNI_Policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy"
  role       = aws_iam_role.wafer-node.name
}

resource "aws_iam_role_policy_attachment" "wafer-node-AmazonEC2ContainerRegistryReadOnly" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
  role       = aws_iam_role.wafer-node.name
}

resource "aws_eks_node_group" "wafer" {
  cluster_name    = aws_eks_cluster.wafer.name
  node_group_name = var.eks_node_group_name
  node_role_arn   = aws_iam_role.wafer-node.arn
  instance_types = [var.clutser_instance_type]
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

resource "aws_vpc" "wafer" {
  cidr_block = var.cluster_vpc_cidr_block

  tags = tomap({
    "Name"                                      = var.cluster_vpc_tag_name,
    "kubernetes.io/cluster/${var.cluster-name}" = "shared",
  })
}

resource "aws_subnet" "wafer" {
  count = 2

  availability_zone       = data.aws_availability_zones.available.names[count.index]
  cidr_block              = "10.0.${count.index}.0/24"
  map_public_ip_on_launch = true
  vpc_id                  = aws_vpc.wafer.id

  tags = tomap({
    "Name"                                      = var.cluster_subnet_tag_name,
    "kubernetes.io/cluster/${var.cluster-name}" = "shared",
  })
}

resource "aws_internet_gateway" "wafer" {
  vpc_id = aws_vpc.wafer.id

  tags = {
    Name = var.cluster_internet_gateway_tag_name
  }
}

resource "aws_route_table" "wafer" {
  vpc_id = aws_vpc.wafer.id

  route {
    cidr_block = var.route_table_cidr_block
    gateway_id = aws_internet_gateway.wafer.id
  }
}

resource "aws_route_table_association" "wafer" {
  count = 2

  subnet_id      = aws_subnet.wafer.*.id[count.index]
  route_table_id = aws_route_table.wafer.id
}