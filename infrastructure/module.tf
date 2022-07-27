terraform {
  backend "s3" {
    bucket = "wafer-tf-state-sethu"
    key    = "tf_state"
    region = "us-east-1"
  }
}

module "mongodb_database" {
  source = "./wafer_database"
}

module "jenkins_instance" {
  source = "./ec2_instances/wafer_jenkins_instance"
}

module "mlflow_instance" {
  source = "./ec2_instances/wafer_mlflow_instance"
}

module "ansible_instance" {
  source = "./ec2_instances/wafer_ansible_instance"
}

module "application_instance" {
  source = "./ec2_instances/wafer_application_instance"
}

module "eks_cluster" {
  source = "./wafer_eks_cluster"
}

module "feature_store_bucket" {
  source = "./s3_buckets/wafer_feature_store_bucket"
}

module "io_files_bucket" {
  source = "./s3_buckets/wafer_io_files_bucket"
}

module "logs_bucket" {
  source = "./s3_buckets/wafer_logs_bucket"
}

module "mlflow_bucket" {
  source = "./s3_buckets/wafer_mlflow_bucket"
}

module "model_bucket" {
  source = "./s3_buckets/wafer_model_bucket"
}

module "pred_data_bucket" {
  source = "./s3_buckets/wafer_pred_data_bucket"
}

module "raw_data_bucket" {
  source = "./s3_buckets/wafer_raw_data_bucket"
}

module "train_data_bucket" {
  source = "./s3_buckets/wafer_train_data_bucket"
}

module "clustering_ecr_repo" {
  source = "./ecr_repos/wafer_clustering_ecr"
}

module "data_transform_pred_ecr_repo" {
  source = "./ecr_repos/wafer_data_transform_pred_ecr"
}

module "data_transform_train_ecr_repo" {
  source = "./ecr_repos/wafer_data_transform_train_ecr"
}

module "db_operation_pred_ecr_repo" {
  source = "./ecr_repos/wafer_db_operation_pred_ecr"
}

module "db_operation_train_ecr_repo" {
  source = "./ecr_repos/wafer_db_operation_train_ecr"
}

module "model_prediction_ecr_repo" {
  source = "./ecr_repos/wafer_model_prediction_ecr"
}

module "model_training_ecr_repo" {
  source = "./ecr_repos/wafer_model_training_ecr"
}

module "load_prod_model_ecr_repo" {
  source = "./ecr_repos/wafer_load_prod_model_ecr"
}

module "preprocessing_pred_ecr_repo" {
  source = "./ecr_repos/wafer_preprocessing_pred_ecr"
}

module "preprocessing_train_ecr_repo" {
  source = "./ecr_repos/wafer_preprocessing_train_ecr"
}

module "raw_pred_data_validation_ecr_repo" {
  source = "./ecr_repos/wafer_raw_pred_data_validation_ecr"
}

module "raw_train_data_validation_ecr_repo" {
  source = "./ecr_repos/wafer_raw_train_data_validation_ecr"
}
