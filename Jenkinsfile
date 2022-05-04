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

    stage {
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

    stage {
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

    stage {
      environment {
        AWS_ACCESS_KEY_ID = credentials('AWS_ACCESS_KEY_ID')

        AWS_SECRET_ACCESS_KEY = credentials('AWS_SECRET_ACCESS_KEY')

        AWS_DEFAULT_REGION = "us-east-1"
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

    stage {
      environment {
        AWS_ACCESS_KEY_ID = credentials('AWS_ACCESS_KEY_ID')

        AWS_SECRET_ACCESS_KEY = credentials('AWS_SECRET_ACCESS_KEY')

        AWS_DEFAULT_REGION = "us-east-1"
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

    stage {
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

    stage {
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

    stage {
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

    stage {
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

    stage {
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

    stage {
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
  }
}