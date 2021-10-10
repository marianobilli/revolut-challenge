provider "aws" {
  region = "eu-central-1"
}

terraform {
  required_version = "1.0.8"

  required_providers {
    aws        = ">= 3.62"
    kubernetes = ">= 2.4.1"
    kubectl = {
      source  = "gavinbunney/kubectl"
      version = ">= 1.11.3"
    }
    flux = {
      source  = "fluxcd/flux"
      version = ">= 0.3.1"
    }
  }

  backend "s3" {
    bucket         = "mbilling-revolut-challenge-tfstate"
    key            = "main.tfstate"
    region         = "eu-central-1"
    dynamodb_table = "terraform-lock"
  }
}

locals {
  iam_policies = yamldecode(file("values/iam_policies.yaml"))
  rds          = yamldecode(file("values/rds.yaml"))
  sg           = yamldecode(file("values/sg.yaml"))
  network      = yamldecode(file("values/network.yaml"))
  eks = yamldecode(templatefile("./values/eks.yaml", {
    subnet_a = aws_subnet.public["eu-central-1a"].id
    subnet_b = aws_subnet.public["eu-central-1b"].id
  }))
  iam_roles_eks = yamldecode(file("values/iam_roles_eks.yaml"))
}
