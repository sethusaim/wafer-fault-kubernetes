pipeline {
  agent any

  stages {
    stage('Cloning Git') {
      steps {
        git branch: 'main', url: 'https://github.com/sethusaim/Wafer-Fault-Kubernetes.git'
      }
    }

    stage('Build and Push Application Service') {
      environment {
        AWS_ACCOUNT_ID = credentials('AWS_ACCOUNT_ID')

        AWS_ACCESS_KEY_ID = credentials('AWS_ACCESS_KEY_ID')

        AWS_SECRET_ACCESS_KEY = credentials('AWS_SECRET_ACCESS_KEY')

        KFP_HOST = credentials('KFP_HOST')

        AWS_DEFAULT_REGION = "us-east-1"
      }

      when {
        changeset 'application/*'
      }

      steps {
        script {
          sh 'aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com'

          sh 'docker build -t wafer-application application/'

          sh 'docker tag wafer-application:latest ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/wafer-application:${BUILD_NUMBER}'

          sh 'docker push ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/wafer-application:${BUILD_NUMBER}'
        }
      }
    }

    stage('Build and Push Clustering Service') {
      environment {
        AWS_ACCESS_KEY_ID = credentials('AWS_ACCESS_KEY_ID')

        AWS_SECRET_ACCESS_KEY = credentials('AWS_SECRET_ACCESS_KEY')

        AWS_DEFAULT_REGION = "us-east-1"
      }

      when {
        changeset 'clustering/*'
      }

      steps {
        script {
          sh 'aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com'

          sh 'docker build -t wafer-clustering clustering/'

          sh 'docker tag wafer-clustering:latest ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/wafer-clustering:${BUILD_NUMBER}'

          sh 'docker push ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/wafer-clustering:${BUILD_NUMBER}'
        }
      }
    }

    stage('Build and Push Data Transformation Prediction Service') {
      environment {
        AWS_ACCESS_KEY_ID = credentials('AWS_ACCESS_KEY_ID')

        AWS_SECRET_ACCESS_KEY = credentials('AWS_SECRET_ACCESS_KEY')

        AWS_DEFAULT_REGION = "us-east-1"
      }

      when {
        changeset 'data_transform_pred/*'
      }

      steps {
        script {
          sh 'aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com'

          sh 'docker build -t wafer-data_transform_pred data_transform_pred/'

          sh 'docker tag wafer-data_transform_pred:latest ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/wafer-data_transform_pred:${BUILD_NUMBER}'

          sh 'docker push ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/wafer-data_transform_pred:${BUILD_NUMBER}'
        }
      }
    }

    stage('Build and Push Data Transformation Train Service') {
      environment {
        AWS_ACCESS_KEY_ID = credentials('AWS_ACCESS_KEY_ID')

        AWS_SECRET_ACCESS_KEY = credentials('AWS_SECRET_ACCESS_KEY')

        AWS_DEFAULT_REGION = "us-east-1"
      }

      when {
        changeset 'data_transform_train/*'
      }

      steps {
        sh 'aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com'

        sh 'docker build -t wafer-data_transform_train data_transform_train/'

        sh 'docker tag wafer-data_transform_train:latest ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/wafer-data_transform_train:${BUILD_NUMBER}'

        sh 'docker push ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/wafer-data_transform_train:${BUILD_NUMBER}'
      }
    }

    stage('Build and Push Database Operation Prediction Service') {
      environment {
        AWS_ACCESS_KEY_ID = credentials('AWS_ACCESS_KEY_ID')

        AWS_SECRET_ACCESS_KEY = credentials('AWS_SECRET_ACCESS_KEY')

        AWS_DEFAULT_REGION = "us-east-1"

        MONGODB_URL = credentials('MONGODB_URL')
      }

      when {
        changeset 'db_operation_pred/*'
      }

      steps {
        sh 'aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com'

        sh 'docker build -t wafer-db_operation_pred db_operation_pred/'

        sh 'docker tag wafer-db_operation_pred:latest ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/wafer-db_operation_pred:${BUILD_NUMBER}'

        sh 'docker push ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/wafer-db_operation_pred:${BUILD_NUMBER}'
      }
    }

    stage('Build and Push Database Operation Training Service') {
      environment {
        AWS_ACCESS_KEY_ID = credentials('AWS_ACCESS_KEY_ID')

        AWS_SECRET_ACCESS_KEY = credentials('AWS_SECRET_ACCESS_KEY')

        AWS_DEFAULT_REGION = "us-east-1"

        MONGODB_URL = credentials('MONGODB_URL')
      }

      when {
        changeset 'db_operation_train/*'
      }

      steps {
        sh 'aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com'

        sh 'docker build -t wafer-db_operation_train db_operation_train/'

        sh 'docker tag wafer-db_operation_train:latest ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/wafer-db_operation_pred:${BUILD_NUMBER}'

        sh 'docker push ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/wafer-db_operation_train:${BUILD_NUMBER}'
      }
    }

    stage('Build and Push Load Production Model Service') {
      environment {
        AWS_ACCESS_KEY_ID = credentials('AWS_ACCESS_KEY_ID')

        AWS_SECRET_ACCESS_KEY = credentials('AWS_SECRET_ACCESS_KEY')

        AWS_DEFAULT_REGION = "us-east-1"

        MLFLOW_TRACKING_URI = credentials('MLFLOW_TRACKING_URI')
      }

      when {
        changeset 'load_prod_model/*'
      }

      steps {
        sh 'aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com'

        sh 'docker build -t wafer-load_prod_model load_prod_model/'

        sh 'docker tag wafer-load_prod_model:latest ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/wafer-load_prod_model:${BUILD_NUMBER}'

        sh 'docker push ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/wafer-load_prod_model:${BUILD_NUMBER}'
      }

    }

    stage('Build and Push Model Prediction Service') {
      environment {
        AWS_ACCESS_KEY_ID = credentials('AWS_ACCESS_KEY_ID')

        AWS_SECRET_ACCESS_KEY = credentials('AWS_SECRET_ACCESS_KEY')

        AWS_DEFAULT_REGION = "us-east-1"

        MLFLOW_TRACKING_URI = credentials('MLFLOW_TRACKING_URI')

        MLFLOW_TRACKING_USERNAME = credentials('MLFLOW_TRACKING_USERNAME')

        MLFLOW_TRACKING_PASSWORD = credentials('MLFLOW_TRACKING_PASSWORD')
      }

      when {
        changeset 'model_prediction/*'
      }

      steps {
        sh 'aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com'

        sh 'docker build -t wafer-model_prediction model_prediction/'

        sh 'docker tag wafer-model_prediction:latest ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/wafer-model_prediction:${BUILD_NUMBER}'

        sh 'docker push ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/wafer-model_prediction:${BUILD_NUMBER}'
      }

    }

    stage('Build and Push Model Training Service') {
      environment {
        AWS_ACCESS_KEY_ID = credentials('AWS_ACCESS_KEY_ID')

        AWS_SECRET_ACCESS_KEY = credentials('AWS_SECRET_ACCESS_KEY')

        AWS_DEFAULT_REGION = "us-east-1"

      }

      when {
        changeset 'model_training/*'
      }

      steps {
        sh 'aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com'

        sh 'docker build -t wafer-model_training model_training/'

        sh 'docker tag wafer-model_training:latest ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/wafer-model_training:${BUILD_NUMBER}'

        sh 'docker push ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/wafer-model_training:${BUILD_NUMBER}'
      }

    }

    stage("Build and Push Preprocessing Prediction Service") {
      environment {
        AWS_ACCESS_KEY_ID = credentials('AWS_ACCESS_KEY_ID')

        AWS_SECRET_ACCESS_KEY = credentials('AWS_SECRET_ACCESS_KEY')

        AWS_DEFAULT_REGION = "us-east-1"
      }

      when {
        changeset 'preprocessing_pred/*'
      }

      steps {
        sh 'aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com'

        sh 'docker build -t wafer-preprocessing_pred preprocessing_pred/'

        sh 'docker tag wafer-preprocessing_pred:latest ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/wafer-preprocessing_pred:${BUILD_NUMBER}'

        sh 'docker push ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/wafer-preprocessing_pred:${BUILD_NUMBER}'
      }

    }

    stage('Build and Push Preprocessing Train Service') {
      environment {
        AWS_ACCESS_KEY_ID = credentials('AWS_ACCESS_KEY_ID')

        AWS_SECRET_ACCESS_KEY = credentials('AWS_SECRET_ACCESS_KEY')

        AWS_DEFAULT_REGION = "us-east-1"
      }

      when {
        changeset 'preprocessing_train/*'
      }

      steps {
        sh 'aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com'

        sh 'docker build -t wafer-preprocessing_train preprocessing_train/'

        sh 'docker tag wafer-preprocessing_train:latest ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/wafer-preprocessing_train:${BUILD_NUMBER}'

        sh 'docker push ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/wafer-preprocessing_train:${BUILD_NUMBER}'
      }

    }

    stage('Build and Push Raw Prediction Data Validation Service') {
      environment {
        AWS_ACCESS_KEY_ID = credentials('AWS_ACCESS_KEY_ID')

        AWS_SECRET_ACCESS_KEY = credentials('AWS_SECRET_ACCESS_KEY')

        AWS_DEFAULT_REGION = "us-east-1"
      }

      when {
        changeset 'raw_pred_data_validation/*'
      }

      steps {
        sh 'aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com'

        sh 'docker build -t wafer-raw_pred_data_validation raw_pred_data_validation/'

        sh 'docker tag wafer-raw_pred_data_validation:latest ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/wafer-raw_pred_data_validation:${BUILD_NUMBER}'

        sh 'docker push ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/wafer-raw_pred_data_validation:${BUILD_NUMBER}'
      }

    }

    stage('Build and Push Raw Training Data Validation Service') {
      environment {
        AWS_ACCESS_KEY_ID = credentials('AWS_ACCESS_KEY_ID')

        AWS_SECRET_ACCESS_KEY = credentials('AWS_SECRET_ACCESS_KEY')

        AWS_DEFAULT_REGION = "us-east-1"
      }

      when {
        changeset 'raw_train_data_validation/*'
      }

      steps {
        sh 'aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com'

        sh 'docker build -t wafer-raw_train_data_validation raw_train_data_validation/'

        sh 'docker tag wafer-raw_train_data_validation:latest ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/wafer-raw_train_data_validation:${BUILD_NUMBER}'

        sh 'docker push ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/wafer-raw_train_data_validation:${BUILD_NUMBER}'
      }
    }

    stage('Plan and Apply new infrastructure') {
      environment {
        AWS_ACCESS_KEY_ID = credentials('AWS_ACCESS_KEY_ID')

        AWS_SECRET_ACCESS_KEY = credentials('AWS_SECRET_ACCESS_KEY')

        AWS_DEFAULT_REGION = "us-east-1"
      }

      when {
        changeset 'infrastructure/*'
      }

      steps {
        sh 'cd infrastructure'

        sh 'terraform init'

        sh 'terraform fmt'

        sh 'terraform validate'

        sh 'terraform plan'

        sh 'terraform apply --auto-approve'
      }
    }
  }
}