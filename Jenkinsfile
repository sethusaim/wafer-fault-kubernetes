pipeline {
    agent any

    stages {
        stage('Cloning Git')
        {
            checkout([$class: 'GitSCM', branches: [[name: '*/main']], doGenerateSubmoduleConfigurations: false, extensions: [], submoduleCfg: [], userRemoteConfigs: [[credentialsId: '', url: 'https://github.com/sethusaim/Wafer-Fault-Kubernetes.git']]])     
        }

        stage('Build and Push Application') {

            environment {
                AWS_ACCOUNT_ID = credentials('aws-account-id')

                AWS_REGION = credentials("aws-region")   
            }

            steps {
                script {
                    sh 'aws ecr get-login-password --region {AWS_REGION} | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com'

                    sh 'docker build -t wafer-application application/'

                    sh 'docker tag wafer-application:latest ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/wafer-application:${BUILD_NUMBER}'   

                    sh 'docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/wafer-application:${BUILD_NUMBER}'    
                }
            }
        }
    }
}