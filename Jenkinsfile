pipeline {
  agent any

  stages {
    stage('Cloning Git') {
      steps {
        git branch: 'main', url: 'https://github.com/sethusaim/Wafer-Fault-Kubernetes.git'
      }
    }

    stage('Build and Push Application') {
      environment {
        AWS_ACCOUNT_ID = credentials('AWS_ACCOUNT_ID')

        AWS_ACCESS_KEY_ID = credentials('AWS_ACCESS_KEY_ID')

        AWS_SECRET_ACCESS_KEY = credentials('AWS_SECRET_ACCESS_KEY')
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
  }
}