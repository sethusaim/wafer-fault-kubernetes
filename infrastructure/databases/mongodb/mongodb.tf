resource "mongodbatlas_cluster" "cluster-atlas" {
  project_id                   = var.atlasprojectid
  name                         = var.database_name
  cloud_backup                 = var.auto_scaling_disk_gb_enabled
  auto_scaling_disk_gb_enabled = var.cloud_backup
  mongo_db_major_version       = var.mongo_version
  cluster_type                 = var.cluster_type
  replication_specs {
    num_shards = var.num_shards
    regions_config {
      region_name     = var.atlas_region
      electable_nodes = var.electable_nodes
      priority        = var.priority
      read_only_nodes = var.read_only_nodes
    }
  }

  provider_name               = var.provider_name
  disk_size_gb                = var.disk_size_gb
  provider_instance_size_name = var.provider_instance_size_name
}

data "mongodbatlas_cluster" "cluster-atlas" {
  project_id = var.atlasprojectid
  name       = mongodbatlas_cluster.cluster-atlas.name
  depends_on = [mongodbatlas_privatelink_endpoint_service.atlaseplink]
}
