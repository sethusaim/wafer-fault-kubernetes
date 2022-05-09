module "jenkins" {
  source = "./jenkins"
}

module "mlflow" {
  source = "./mlflow"
}

module "feature_store" {
  source = "./wafer-feature-store"
}

module "io_files" {
  source = "./wafer-io-files"
}