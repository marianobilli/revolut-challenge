data "aws_eks_cluster" "cluster" {
  name = module.eks_cluster.cluster_id
}

data "aws_eks_cluster_auth" "cluster" {
  name = module.eks_cluster.cluster_id
}

provider "kubernetes" {
  host                   = data.aws_eks_cluster.cluster.endpoint
  cluster_ca_certificate = base64decode(data.aws_eks_cluster.cluster.certificate_authority.0.data)
  token                  = data.aws_eks_cluster_auth.cluster.token
}

module "eks_cluster" {
  source  = "terraform-aws-modules/eks/aws"
  version = "17.15.0"

  write_kubeconfig            = false
  cluster_name                = "revolut"
  cluster_version             = local.eks.control_plane.cluster_version
  subnets                     = [for subnet in aws_subnet.public : subnet.id]
  vpc_id                      = aws_vpc.main.id
  enable_irsa                 = true
  manage_worker_iam_resources = true

  # Private cluster
  cluster_endpoint_public_access = true
  cluster_endpoint_private_access = true
  cluster_create_endpoint_private_access_sg_rule = true
  cluster_endpoint_private_access_cidrs = local.eks.control_plane.cluster_endpoint_private_access_cidrs

  # aws-auth config-map
  manage_aws_auth = true

  # Compute
  worker_additional_security_group_ids = [for sg in local.eks.worker_additional_security_group_ids : aws_security_group.main[sg].id]
  node_groups_defaults                 = local.eks.node_groups_defaults
  node_groups                          = local.eks.node_groups

  depends_on = [ aws_security_group.main, aws_subnet.public, aws_vpc.main ]
}
