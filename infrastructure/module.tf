module "jenkins_instance" {
  source = "./jenkins_instance"
}

module "mlflow_instance" {
  source = "./mlflow_instance"
}

module "eks_cluster" {
  source = "./wafer_eks_cluster"
}

module "feature_store_bucket" {
  source = "./wafer_feature_store_bucket"
}

module "io_files_bucket" {
  source = "./wafer_io_files_bucket"
}

module "kube_master" {
  source = "./wafer_kube_master"
}

module "kubeflow_components_bucket" {
  source = "./wafer_kubeflow_components_bucket"
}

module "logs_bucket" {
  source = "./wafer_logs_bucket"
}

module "mlflow_bucket" {
  source = "./wafer_mlflow_bucket"
}

module "model_bucket" {
  source = "./wafer_model_bucket"
}

module "pred_data_bucket" {
  source = "./wafer_pred_data_bucket"
}

module "raw_data_bucket" {
  source = "./wafer_raw_data_bucket"
}

module "train_data_bucket" {
  source = "./wafer_train_data_bucket"
}

