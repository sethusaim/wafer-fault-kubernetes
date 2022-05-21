pipeline {
  agent any

  stages {
    stage('Cloning Git') {
      steps {
        git branch: 'main', url: 'https://github.com/sethusaim/Wafer-Fault-Kubernetes.git'
      }
    }

    stage("Build and Push Application Service") {
      environment {
        AWS_ACCOUNT_ID = credentials('AWS_ACCOUNT_ID')

        AWS_ACCESS_KEY_ID = credentials('AWS_ACCESS_KEY_ID')

        AWS_SECRET_ACCESS_KEY = credentials('AWS_SECRET_ACCESS_KEY')

        AWS_DEFAULT_REGION = "us-east-1"

        REPO_NAME = "wafer_application"

        COMP_FILE = "wafer_application.yaml"
      }

      when {
        changeset 'application/*'
      }

      steps {
        script {
          sh 'aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com'

          sh 'docker build --build-arg AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} --build-arg AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} --build-arg AWS_DEFAULT_REGION=${AWS_DEFAULT_REGION} -t $REPO_NAME application/'

          sh 'docker tag $REPO_NAME:latest ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/$REPO_NAME:${BUILD_NUMBER}'

          sh 'docker push ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/$REPO_NAME:${BUILD_NUMBER}'
        }

        sshagent(credentials: ['id_name_added_underManageCredential']) {

          sh "ssh command"

        }
      }

      stage('Build and Push Clustering Service') {
        environment {
          AWS_ACCOUNT_ID = credentials('AWS_ACCOUNT_ID')

          AWS_ACCESS_KEY_ID = credentials('AWS_ACCESS_KEY_ID')

          AWS_SECRET_ACCESS_KEY = credentials('AWS_SECRET_ACCESS_KEY')

          AWS_DEFAULT_REGION = "us-east-1"

          REPO_NAME = "wafer_clustering"

          COMP_FILE = "wafer_clustering.yaml"
        }

        when {
          changeset 'clustering/*'
        }

        steps {
          script {
            sh 'aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com'

            sh 'docker build --build-arg AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} --build-arg AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} --build-arg AWS_DEFAULT_REGION=${AWS_DEFAULT_REGION} -t $REPO_NAME clustering/'

            sh 'docker tag $REPO_NAME:latest ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/$REPO_NAME:${BUILD_NUMBER}'

            sh 'docker push ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/$REPO_NAME:${BUILD_NUMBER}'
          }

          build job: 'updatemanifest', parameters: [string(name: 'DOCKERTAG', value: env.BUILD_NUMBER), string(name: 'REPO_NAME', value: env.REPO_NAME), string(name: 'COMP_FILE', value: env.COMP_FILE)]
        }
      }

      stage('Build and Push Data Transformation Prediction Service') {
        environment {
          AWS_ACCESS_KEY_ID = credentials('AWS_ACCESS_KEY_ID')

          AWS_SECRET_ACCESS_KEY = credentials('AWS_SECRET_ACCESS_KEY')

          AWS_ACCOUNT_ID = credentials('AWS_ACCOUNT_ID')

          AWS_DEFAULT_REGION = "us-east-1"

          REPO_NAME = "wafer_data_transform_pred"

          COMP_FILE = "wafer_data_transform_pred.yaml"
        }

        when {
          changeset 'data_transform_pred/*'
        }

        steps {
          script {
            sh 'aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com'

            sh 'docker build --build-arg AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} --build-arg AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} --build-arg AWS_DEFAULT_REGION=${AWS_DEFAULT_REGION} -t $REPO_NAME data_transform_pred/'

            sh 'docker tag $REPO_NAME:latest ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/$REPO_NAME:${BUILD_NUMBER}'

            sh 'docker push ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/$REPO_NAME:${BUILD_NUMBER}'
          }

          build job: 'updatemanifest', parameters: [string(name: 'DOCKERTAG', value: env.BUILD_NUMBER), string(name: 'REPO_NAME', value: env.REPO_NAME), string(name: 'COMP_FILE', value: env.COMP_FILE)]
        }
      }

      stage('Build and Push Data Transformation Train Service') {
        environment {
          AWS_ACCESS_KEY_ID = credentials('AWS_ACCESS_KEY_ID')

          AWS_SECRET_ACCESS_KEY = credentials('AWS_SECRET_ACCESS_KEY')

          AWS_ACCOUNT_ID = credentials('AWS_ACCOUNT_ID')

          AWS_DEFAULT_REGION = "us-east-1"

          REPO_NAME = "wafer_data_transform_train"

          COMP_FILE = "wafer_data_transform_train.yaml"
        }

        when {
          changeset 'data_transform_train/*'
        }

        steps {
          script {
            sh 'aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com'

            sh 'docker build --build-arg AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} --build-arg AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} --build-arg AWS_DEFAULT_REGION=${AWS_DEFAULT_REGION} -t $REPO_NAME data_transform_train/'

            sh 'docker tag $REPO_NAME:latest ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/$REPO_NAME:${BUILD_NUMBER}'

            sh 'docker push ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/$REPO_NAME:${BUILD_NUMBER}'
          }

          build job: 'updatemanifest', parameters: [string(name: 'DOCKERTAG', value: env.BUILD_NUMBER), string(name: 'REPO_NAME', value: env.REPO_NAME), string(name: 'COMP_FILE', value: env.COMP_FILE)]

        }
      }

      stage('Build and Push Database Operation Prediction Service') {
        environment {
          AWS_ACCESS_KEY_ID = credentials('AWS_ACCESS_KEY_ID')

          AWS_SECRET_ACCESS_KEY = credentials('AWS_SECRET_ACCESS_KEY')

          AWS_ACCOUNT_ID = credentials('AWS_ACCOUNT_ID')

          AWS_DEFAULT_REGION = "us-east-1"

          MONGODB_URL = credentials('MONGODB_URL')

          REPO_NAME = "wafer_db_operation_pred"

          COMP_FILE = "wafer_db_operation_pred.yaml"
        }

        when {
          changeset 'db_operation_pred/*'
        }

        steps {
          script {
            sh 'aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com'

            sh 'docker build --build-arg MONGODB_URL=${MONGODB_URL} --build-arg AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} --build-arg AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} --build-arg AWS_DEFAULT_REGION=${AWS_DEFAULT_REGION} -t $REPO_NAME db_operation_pred/'

            sh 'docker tag $REPO_NAME:latest ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/$REPO_NAME:${BUILD_NUMBER}'

            sh 'docker push ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/$REPO_NAME:${BUILD_NUMBER}'
          }

          build job: 'updatemanifest', parameters: [string(name: 'DOCKERTAG', value: env.BUILD_NUMBER), string(name: 'REPO_NAME', value: env.REPO_NAME), string(name: 'COMP_FILE', value: env.COMP_FILE)]
        }
      }

      stage('Build and Push Database Operation Training Service') {
        environment {
          AWS_ACCESS_KEY_ID = credentials('AWS_ACCESS_KEY_ID')

          AWS_SECRET_ACCESS_KEY = credentials('AWS_SECRET_ACCESS_KEY')

          AWS_ACCOUNT_ID = credentials('AWS_ACCOUNT_ID')

          AWS_DEFAULT_REGION = "us-east-1"

          MONGODB_URL = credentials('MONGODB_URL')

          REPO_NAME = "wafer_db_operation_train"

          COMP_FILE = "wafer_db_operation_train.yaml"
        }

        when {
          changeset 'db_operation_train/*'
        }

        steps {
          script {
            sh 'aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com'

            sh 'docker build --build-arg MONGODB_URL=${MONGODB_URL} --build-arg AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} --build-arg AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} --build-arg AWS_DEFAULT_REGION=${AWS_DEFAULT_REGION} -t $REPO_NAME db_operation_train/'

            sh 'docker tag $REPO_NAME:latest ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/$REPO_NAME:${BUILD_NUMBER}'

            sh 'docker push ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/$REPO_NAME:${BUILD_NUMBER}'
          }

          build job: 'updatemanifest', parameters: [string(name: 'DOCKERTAG', value: env.BUILD_NUMBER), string(name: 'REPO_NAME', value: env.REPO_NAME), string(name: 'COMP_FILE', value: env.COMP_FILE)]

        }
      }

      stage('Build and Push Load Production Model Service') {
        environment {
          AWS_ACCESS_KEY_ID = credentials('AWS_ACCESS_KEY_ID')

          AWS_SECRET_ACCESS_KEY = credentials('AWS_SECRET_ACCESS_KEY')

          AWS_ACCOUNT_ID = credentials('AWS_ACCOUNT_ID')

          AWS_DEFAULT_REGION = "us-east-1"

          MLFLOW_TRACKING_URI = credentials('MLFLOW_TRACKING_URI')

          REPO_NAME = "wafer_load_prod_model"

          COMP_FILE = "wafer_load_prod_model.yaml"
        }

        when {
          changeset 'load_prod_model/*'
        }

        steps {
          script {
            sh 'aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com'

            sh 'docker build --build-arg MLFLOW_TRACKING_URI=${MLFLOW_TRACKING_URI} --build-arg AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} --build-arg AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} --build-arg AWS_DEFAULT_REGION=${AWS_DEFAULT_REGION} load_prod_model/'

            sh 'docker tag $REPO_NAME:latest ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/$REPO_NAME:${BUILD_NUMBER}'

            sh 'docker push ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/$REPO_NAME:${BUILD_NUMBER}'
          }

          build job: 'updatemanifest', parameters: [string(name: 'DOCKERTAG', value: env.BUILD_NUMBER), string(name: 'REPO_NAME', value: env.REPO_NAME), string(name: 'COMP_FILE', value: env.COMP_FILE)]

        }

      }

      stage('Build and Push Model Prediction Service') {
        environment {
          AWS_ACCESS_KEY_ID = credentials('AWS_ACCESS_KEY_ID')

          AWS_SECRET_ACCESS_KEY = credentials('AWS_SECRET_ACCESS_KEY')

          AWS_ACCOUNT_ID = credentials('AWS_ACCOUNT_ID')

          AWS_DEFAULT_REGION = "us-east-1"

          REPO_NAME = "wafer_model_prediction"

          COMP_FILE = "wafer_load_prod_model.yaml"
        }

        when {
          changeset 'model_prediction/*'
        }

        steps {
          script {
            sh 'aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com'

            sh 'docker build --build-arg AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} --build-arg AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} --build-arg AWS_DEFAULT_REGION=${AWS_DEFAULT_REGION} -t $REPO_NAME model_prediction/'

            sh 'docker tag $REPO_NAME:latest ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/$REPO_NAME:${BUILD_NUMBER}'

            sh 'docker push ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/$REPO_NAME:${BUILD_NUMBER}'

          }

          build job: 'updatemanifest', parameters: [string(name: 'DOCKERTAG', value: env.BUILD_NUMBER), string(name: 'REPO_NAME', value: env.REPO_NAME), string(name: 'COMP_FILE', value: env.COMP_FILE)]

        }

      }

      stage('Build and Push Model Training Service') {
        environment {
          AWS_ACCESS_KEY_ID = credentials('AWS_ACCESS_KEY_ID')

          AWS_SECRET_ACCESS_KEY = credentials('AWS_SECRET_ACCESS_KEY')

          AWS_ACCOUNT_ID = credentials('AWS_ACCOUNT_ID')

          AWS_DEFAULT_REGION = "us-east-1"

          MLFLOW_TRACKING_URI = credentials("MLFLOW_TRACKING_URI")

          MLFLOW_TRACKING_USERNAME = credentials("MLFLOW_TRACKING_USERNAME")

          MLFLOW_TRACKING_PASSWORD = credentials("MLFLOW_TRACKING_PASSWORD")

          REPO_NAME = "wafer_model_training"

          COMP_FILE = "wafer_model_training.yaml"
        }

        when {
          changeset 'model_training/*'
        }

        steps {
          script {
            sh 'aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com'

            sh 'docker build --build-arg MLFLOW_TRACKING_URI=${MLFLOW_TRACKING_URI} --build-arg MLFLOW_TRACKING_USERNAME=${MLFLOW_TRACKING_USERNAME} --build-arg MLFLOW_TRACKING_PASSWORD=${MLFLOW_TRACKING_PASSWORD} --build-arg AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} --build-arg AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} --build-arg AWS_DEFAULT_REGION=${AWS_DEFAULT_REGION} -t $REPO_NAME model_training/'

            sh 'docker tag $REPO_NAME:latest ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/$REPO_NAME:${BUILD_NUMBER}'

            sh 'docker push ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/$REPO_NAME:${BUILD_NUMBER}'
          }

          build job: 'updatemanifest', parameters: [string(name: 'DOCKERTAG', value: env.BUILD_NUMBER), string(name: 'REPO_NAME', value: env.REPO_NAME), string(name: 'COMP_FILE', value: env.COMP_FILE)]

        }
      }

      stage("Build and Push Preprocessing Prediction Service") {
        environment {
          AWS_ACCESS_KEY_ID = credentials('AWS_ACCESS_KEY_ID')

          AWS_SECRET_ACCESS_KEY = credentials('AWS_SECRET_ACCESS_KEY')

          AWS_ACCOUNT_ID = credentials('AWS_ACCOUNT_ID')

          AWS_DEFAULT_REGION = "us-east-1"

          REPO_NAME = "wafer_preprocessing_pred"

          COMP_FILE = "wafer_preprocessing_pred.yaml"
        }

        when {
          changeset 'preprocessing_pred/*'
        }

        steps {
          script {
            sh 'aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com'

            sh 'docker build --build-arg AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} --build-arg AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} --build-arg AWS_DEFAULT_REGION=${AWS_DEFAULT_REGION} -t $REPO_NAME preprocessing_pred/'

            sh 'docker tag $REPO_NAME:latest ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/$REPO_NAME:${BUILD_NUMBER}'

            sh 'docker push ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/$REPO_NAME:${BUILD_NUMBER}'
          }

          build job: 'updatemanifest', parameters: [string(name: 'DOCKERTAG', value: env.BUILD_NUMBER), string(name: 'REPO_NAME', value: env.REPO_NAME), string(name: 'COMP_FILE', value: env.COMP_FILE)]

        }

      }

      stage('Build and Push Preprocessing Train Service') {
        environment {
          AWS_ACCESS_KEY_ID = credentials('AWS_ACCESS_KEY_ID')

          AWS_SECRET_ACCESS_KEY = credentials('AWS_SECRET_ACCESS_KEY')

          AWS_ACCOUNT_ID = credentials('AWS_ACCOUNT_ID')

          AWS_DEFAULT_REGION = "us-east-1"

          REPO_NAME = "wafer_preprocessing_train"

          COMP_FILE = "wafer_preprocessing_train.yaml"
        }

        when {
          changeset 'preprocessing_train/*'
        }

        steps {
          script {
            sh 'aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com'

            sh 'docker build --build-arg AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} --build-arg AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} --build-arg AWS_DEFAULT_REGION=${AWS_DEFAULT_REGION} -t $REPO_NAME preprocessing_train/'

            sh 'docker tag $REPO_NAME:latest ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/$REPO_NAME:${BUILD_NUMBER}'

            sh 'docker push ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/$REPO_NAME:${BUILD_NUMBER}'
          }

          build job: 'updatemanifest', parameters: [string(name: 'DOCKERTAG', value: env.BUILD_NUMBER), string(name: 'REPO_NAME', value: env.REPO_NAME), string(name: 'COMP_FILE', value: env.COMP_FILE)]
        }
      }

      stage('Build and Push Raw Prediction Data Validation Service') {
        environment {
          AWS_ACCESS_KEY_ID = credentials('AWS_ACCESS_KEY_ID')

          AWS_SECRET_ACCESS_KEY = credentials('AWS_SECRET_ACCESS_KEY')

          AWS_ACCOUNT_ID = credentials('AWS_ACCOUNT_ID')

          AWS_DEFAULT_REGION = "us-east-1"

          REPO_NAME = "wafer_raw_pred_data_validation"

          COMP_FILE = "wafer_raw_pred_data_validation.yaml"
        }

        when {
          changeset 'raw_pred_data_validation/*'
        }

        steps {
          script {
            sh 'aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com'

            sh 'docker build --build-arg AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} --build-arg AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} --build-arg AWS_DEFAULT_REGION=${AWS_DEFAULT_REGION} -t $REPO_NAME raw_pred_data_validation/'

            sh 'docker tag $REPO_NAME:latest ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/$REPO_NAME:${BUILD_NUMBER}'

            sh 'docker push ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/$REPO_NAME:${BUILD_NUMBER}'
          }

          build job: 'updatemanifest', parameters: [string(name: 'DOCKERTAG', value: env.BUILD_NUMBER), string(name: 'REPO_NAME', value: env.REPO_NAME), string(name: 'COMP_FILE', value: env.COMP_FILE)]

        }

      }

      stage('Build and Push Raw Training Data Validation Service') {
        environment {
          AWS_ACCESS_KEY_ID = credentials('AWS_ACCESS_KEY_ID')

          AWS_SECRET_ACCESS_KEY = credentials('AWS_SECRET_ACCESS_KEY')

          AWS_ACCOUNT_ID = credentials('AWS_ACCOUNT_ID')

          AWS_DEFAULT_REGION = "us-east-1"

          REPO_NAME = "wafer_raw_train_data_validation"

          COMP_FILE = "wafer_raw_train_data_validation.yaml"
        }

        when {
          changeset 'raw_train_data_validation/*'
        }

        steps {
          script {
            sh 'aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com'

            sh 'docker build --build-arg AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} --build-arg AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} --build-arg AWS_DEFAULT_REGION=${AWS_DEFAULT_REGION} -t $REPO_NAME raw_train_data_validation/'

            sh 'docker tag $REPO_NAME:latest ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/$REPO_NAME:${BUILD_NUMBER}'

            sh 'docker push ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/$REPO_NAME:${BUILD_NUMBER}'
          }

          build job: 'updatemanifest', parameters: [string(name: 'DOCKERTAG', value: env.BUILD_NUMBER), string(name: 'REPO_NAME', value: env.REPO_NAME), string(name: 'COMP_FILE', value: env.COMP_FILE)]
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
          script {
            sh 'terraform -chdir=infrastructure init'

            sh 'terraform -chdir=infrastructure apply --auto-approve'
          }
        }
      }
    }
  }