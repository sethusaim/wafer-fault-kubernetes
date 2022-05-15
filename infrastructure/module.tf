module "jenkins_instance" {
  source = "./wafer_jenkins_instance"
}

# module "mlflow_instance" {
#   source = "./wafer_mlflow_instance"
# }

# module "eks_cluster" {
#   source = "./wafer_eks_cluster"
# }

module "feature_store_bucket" {
  source = "./wafer_feature_store_bucket"
}

module "io_files_bucket" {
  source = "./wafer_io_files_bucket"
}

# module "kube_master" {
#   source = "./wafer_kube_master"
# }

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

module "app_ecr_repo" {
  source = "./wafer_app_ecr"
}

module "clustering_ecr_repo" {
  source = "./wafer_clustering_ecr"
}

module "data_transform_pred_ecr_repo" {
  source = "./wafer_data_transform_pred_ecr"
}

module "data_transform_train_ecr_repo" {
  source = "./wafer_data_transform_train_ecr"
}

module "db_operation_pred_ecr_repo" {
  source = "./wafer_db_operation_pred_ecr"
}

module "db_operation_train_ecr_repo" {
  source = "./wafer_db_operation_train_ecr"
}

module "model_predcition_ecr_repo" {
  source = "./wafer_model_prediction_ecr"
}

module "model_training_ecr_repo" {
  source = "./wafer_model_training_ecr"
}

module "preprocessing_pred_ecr_repo" {
  source = "./wafer_preprocessing_pred_ecr"
}

module "preprocessing_train_ecr_repo" {
  source = "./wafer_preprocessing_train_ecr"
}

module "raw_pred_data_validation_ecr_repo" {
  source = "./wafer_raw_pred_data_validation_ecr"
}

module "raw_train_data_validation_ecr_repo" {
  source = "./wafer_raw_train_data_validation_ecr"
}

