locals {
  namespace = "flux-system"
}

data "flux_install" "main" {
  target_path    = terraform.workspace
  network_policy = false
  version        = "v0.17.1"
}

# Split multi-doc YAML with
data "kubectl_file_documents" "main" {
  content = data.flux_install.main.content
}

# Store the yaml files locally
resource "local_file" "flux_install" {
    for_each   = { for yaml in data.kubectl_file_documents.main.documents : lower(join("/", compact([yamldecode(yaml).kind, yamldecode(yaml).metadata.name]))) => yaml }
    content     = each.value
    filename = "../kubernetes/flux-system/flux/${each.key}.yaml"
}

# revolut SYNC
data "flux_sync" "revolut" {
  name        = "revolut"
  namespace   = local.namespace
  target_path = "kubernetes/"
  interval    = 5
  secret      = "github"
  branch      = "main"
  url         = "https://github.com/marianobilli/revolut-challenge.git"
}

# Split multi-doc YAML with
data "kubectl_file_documents" "revolut" {
  content = data.flux_sync.revolut.content
}

# Store the yaml files locally
resource "local_file" "revolut" {
    for_each   = { for yaml in data.kubectl_file_documents.revolut.documents : lower(join("/", compact([yamldecode(yaml).kind, yamldecode(yaml).metadata.name]))) => yaml }
    content     = each.value
    filename = "../kubernetes/flux-system/revolut/${each.key}.yaml"
}