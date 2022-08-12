output "atlasclusterstring" {
  value = data.mongodbatlas_cluster.cluster-atlas.connection_strings
}

output "plstring" {
  value = lookup(data.mongodbatlas_cluster.cluster-atlas.connection_strings[0].aws_private_link_srv, aws_vpc_endpoint.ptfe_service.id)
}