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

module "kubeflow_components" {
  source = "./wafer-kubeflow-components"
}

module "logs" {
  source = "./wafer-logs"
}

module "mlflow" {
  source = "./wafer-mlflow"
}

module "model" {
  source = "./wafer-model"
}

module "pred-data" {
  source = "./wafer-pred-data"
}

module "raw-data" {
  source = "./wafe-raw-data"
}

module "train-data" {
  source = "./wafer-train-data"
}
