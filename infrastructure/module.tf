module "jenkins_instance" {
  source = "./jenkins_instance"
}

module "mlflow_instance" {
  source = "./wafer-mlflow"
}

module "feature_store_bucket" {
  source = "./wafer-feature-store"
}

module "io_files_bucket" {
  source = "./wafer-io-files"
}

module "kubeflow_components_bucket" {
  source = "./wafer-kubeflow-components"
}

module "logs_bucket" {
  source = "./wafer-logs"
}

module "mlflow_bucket" {
  source = "./wafer-mlflow"
}

module "model_bucket" {
  source = "./wafer-model"
}

module "pred-data_bucket" {
  source = "./wafer-pred-data"
}

module "raw-data_bucket" {
  source = "./wafer-raw-data"
}

module "train-data_bucket" {
  source = "./wafer-train-data"
}
