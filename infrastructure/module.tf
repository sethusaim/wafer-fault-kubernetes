module "jenkins" {
  source = "./jenkins"
}

module "mlflow" {
  source = "./mlflow"
}

module "feature_store" {
  source = "./wafer_feature_store"
}
