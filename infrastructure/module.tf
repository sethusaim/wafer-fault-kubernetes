terraform {
  backend "s3" {
    bucket = "sethu-tf-state"
    key    = "tf_state"
    region = "us-east-1"
  }
}

module "truck_artifacts" {
  source = "./truck_artifacts"
}

