provider "aws" {
  region = var.aws_region
}

data "aws_availability_zones" "available" {}

resource "aws_iam_role" "wafer_cluster_iam_role" {
  name = var.wafer_cluster_iam_role_name
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

resource "aws_iam_role_policy_attachment" "wafer_cluster_AmazonEKSClusterPolicy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
  role       = aws_iam_role.wafer_cluster_iam_role.name
}

resource "aws_iam_role_policy_attachment" "wafer_cluster_AmazonEKSVPCResourceController" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSVPCResourceController"
  role       = aws_iam_role.wafer_cluster_iam_role.name
}

resource "aws_security_group" "wafer_cluster_sg_group" {
  name        = var.wafer_cluster_sg_group_name
  description = "Cluster communication with worker nodes"
  vpc_id      = aws_vpc.wafer_vpc.id

  ingress {
    from_port   = var.cluster_ingress_from_port
    to_port     = var.cluster_ingress_to_port
    protocol    = var.cluster_protocol
    cidr_blocks = var.cluster_cidr_block
  }

  egress {
    from_port   = var.cluster_egress_from_port
    to_port     = var.cluster_egress_to_port
    protocol    = var.cluster_protocol
    cidr_blocks = var.cluster_cidr_block
  }

  tags = {
    Name = var.cluster_sg_group_name
  }
}

resource "aws_eks_cluster" "wafer_eks_cluster" {
  name     = var.wafer_cluster_name
  role_arn = aws_iam_role.wafer_cluster_iam_role.arn

  vpc_config {
    security_group_ids = [aws_security_group.wafer_cluster_sg_group.id]
    subnet_ids         = aws_subnet.wafer_subnet[*].id
  }

  depends_on = [
    aws_iam_role_policy_attachment.wafer_cluster_AmazonEKSClusterPolicy,
    aws_iam_role_policy_attachment.wafer_cluster_AmazonEKSVPCResourceController,
  ]
}

resource "aws_iam_role" "wafer_node_iam_role" {
  name = var.cluster_node_iam_role_name
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

resource "aws_iam_role_policy_attachment" "wafer_node_AmazonEKSWorkerNodePolicy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
  role       = aws_iam_role.wafer_node_iam_role.name
}

resource "aws_iam_role_policy_attachment" "wafer_node_AmazonEKS_CNI_Policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy"
  role       = aws_iam_role.wafer_node_iam_role.name
}

resource "aws_iam_role_policy_attachment" "wafer_node_AmazonEC2ContainerRegistryReadOnly" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
  role       = aws_iam_role.wafer_node_iam_role.name
}

resource "aws_eks_node_group" "wafer_eks_node_group" {
  cluster_name    = aws_eks_cluster.wafer_eks_cluster.name
  node_group_name = var.cluster_node_group_name
  node_role_arn   = aws_iam_role.wafer_node_iam_role.arn
  subnet_ids      = aws_subnet.wafer_subnet[*].id

  scaling_config {
    desired_size = var.required_nodes_size
    max_size     = var.max_nodes_size
    min_size     = var.min_nodes_size
  }

  depends_on = [
    aws_iam_role_policy_attachment.wafer_node_AmazonEKSWorkerNodePolicy,
    aws_iam_role_policy_attachment.wafer_node_AmazonEKS_CNI_Policy,
    aws_iam_role_policy_attachment.wafer_node_AmazonEC2ContainerRegistryReadOnly,
  ]
}


resource "aws_vpc" "wafer_vpc" {
  cidr_block = var.cluster_vpc_cidr_block

  tags = tomap({
    "Name"                                      = var.cluster_vpc_node_group_name,
    "kubernetes.io/cluster/${var.wafer_cluster_name}" = "shared",
  })
}

resource "aws_subnet" "wafer_subnet" {
  count = 2

  availability_zone       = data.aws_availability_zones.available.names[count.index]
  cidr_block              = "10.0.${count.index}.0/24"
  map_public_ip_on_launch = true
  vpc_id                  = aws_vpc.wafer_vpc.id

  tags = tomap({
    "Name"                                      = var.cluster_vpc_node_group_name,
    "kubernetes.io/cluster/${var.wafer_cluster_name}" = "shared",
  })
}

resource "aws_internet_gateway" "wafer_internet_gateway" {
  vpc_id = aws_vpc.wafer_vpc.id

  tags = {
    Name = var.cluster_internet_gateway_tag
  }
}

resource "aws_route_table" "wafer_route_table" {
  vpc_id = aws_vpc.wafer_vpc.id

  route {
    cidr_block = var.cluster_cidr_block[0]
    gateway_id = aws_internet_gateway.wafer_internet_gateway.id
  }
}

resource "aws_route_table_association" "wafer_route_table_association" {
  count = 2

  subnet_id      = aws_subnet.wafer_subnet.*.id[count.index]
  route_table_id = aws_route_table.wafer_route_table.id
}
