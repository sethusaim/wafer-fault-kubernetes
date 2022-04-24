pipeline {
  agent {
    kubernetes {
      yamlFile 'builder.yaml'
    }
  }

  stages {
    stage("Clone Repository")
      {
          checkout scm
      }

    stage("Build and Push Application Component")
    {
        when 
        {
            changeset "application/*"
        }
        steps
        {
            container("kaniko")
            {
                script
                {
                    sh '''/kaniko/executor --dockerfile application/Dockerfile \
                                        --context s3://wafer-image-contexts/" \
                                        --destination=aws_account_id.dkr.ecr.region.amazonaws.com/my-repository:${BUILD_NUMBER}"
            '''
                }
            }

        }
    }

    stage("Build and Push Clustering Component")
    {
        when 
        {
            changeset "clustering/*"
        }
        steps
        {
            container("kaniko")
            {
                script
                {
                    sh '''/kaniko/executor --dockerfile clustering/Dockerfile \
                                        --context s3://wafer-image-contexts/" \
                                        --destination=aws_account_id.dkr.ecr.region.amazonaws.com/my-repository:${BUILD_NUMBER}"
                        '''
                }
            }
        }
    }

    stage("Build and Push Data Transform Pred Component")
    {
        when 
        {
            changeset "data_transform_pred/*"
        }
        steps
        {
            container("kaniko")
            {
                script
                {
                    sh '''/kaniko/executor --dockerfile data_transform_pred/Dockerfile \
                                        --context s3://wafer-image-contexts/" \
                                        --destination=aws_account_id.dkr.ecr.region.amazonaws.com/my-repository:${BUILD_NUMBER}"
            '''
                }
            }
        }
    }

    stage("Build and Push Data Transform Train Component")
    {
        when 
        {
            changeset "data_transform_train/*"
        }
        steps
        {
            container("kaniko")
            {
                script
                {
                    sh '''/kaniko/executor --dockerfile data_transform_pred/Dockerfile \
                                        --context s3://wafer-image-contexts/" \
                                        --destination=aws_account_id.dkr.ecr.region.amazonaws.com/my-repository:${BUILD_NUMBER}"
            '''
                }
            }
        }
    }

    stage("Build and Push DB Operation Pred Component")
    {
        when 
        {
            changeset "db_operation_pred/*"
        }
        steps
        {
            container("kaniko")
            {
                script
                {
                    sh '''/kaniko/executor --dockerfile data_transform_train/Dockerfile \
                                        --context s3://wafer-image-contexts/" \
                                        --destination=aws_account_id.dkr.ecr.region.amazonaws.com/my-repository:${BUILD_NUMBER}"
            '''
                }
            }
        }
    }

    stage("Build and Push DB Operation Train Component")
    {
        when 
        {
            changeset "db_operation_train/*"
        }
        steps
        {
            container("kaniko")
            {
                script
                {
                    sh '''/kaniko/executor --dockerfile db_operation_train/Dockerfile \
                                        --context s3://wafer-image-contexts/" \
                                        --destination=aws_account_id.dkr.ecr.region.amazonaws.com/my-repository:${BUILD_NUMBER}"
            '''
                }
            }
        }
    }

    stage("Build and Push DB Operation Pred Component")
    {
        when 
        {
            changeset "db_operation_pred/*"
        }
        steps
        {
            container("kaniko")
            {
                script
                {
                    sh '''/kaniko/executor --dockerfile db_operation_pred/Dockerfile \
                                        --context s3://wafer-image-contexts/" \
                                        --destination=aws_account_id.dkr.ecr.region.amazonaws.com/my-repository:${BUILD_NUMBER}"
            '''
                }
            }
        }
    }

    stage("Build and Push Load Prod Model Component")
    {   
        when 
        {
            changeset "load_prod_model/*"
        }
        steps
        {
            container("kaniko")
            {
                script
                {
                    sh '''/kaniko/executor --dockerfile load_prod_model/Dockerfile \
                                        --context s3://wafer-image-contexts/" \
                                        --destination=aws_account_id.dkr.ecr.region.amazonaws.com/my-repository:${BUILD_NUMBER}"
            '''
                }
            }
        }
    }

    stage("Build and Push Model Prediction Component")
    {
        when 
        {
            changeset "model_prediction/*"
        }
        steps
        {
            container("kaniko")
            {
                script
                {
                    sh '''/kaniko/executor --dockerfile model_prediction/Dockerfile \
                                        --context s3://wafer-image-contexts/" \
                                        --destination=aws_account_id.dkr.ecr.region.amazonaws.com/my-repository:${BUILD_NUMBER}"
            '''
                }
            }
        }
    }

    stage("Build and Push Model Training Component")
    {
        when 
        {
            changeset "model_training/*"
        }
        steps
        {
            container("kaniko")
            {
                script
                {
                    sh '''/kaniko/executor --dockerfile model_training/Dockerfile \
                                        --context s3://wafer-image-contexts/" \
                                        --destination=aws_account_id.dkr.ecr.region.amazonaws.com/my-repository:${BUILD_NUMBER}"
            '''
                }
            }
        }
    }

    stage("Build and Push Preprocessing Pred Component")
    {
        when 
        {
            changeset "preprocessing_pred/*"
        }
        steps
        {
            container("kaniko")
            {
                script
                {
                    sh '''/kaniko/executor --dockerfile preprocessing_pred/Dockerfile \
                                        --context s3://wafer-image-contexts/" \
                                        --destination=aws_account_id.dkr.ecr.region.amazonaws.com/my-repository:${BUILD_NUMBER}"
            '''
                }
            }
        }
    }

    stage("Build and Push Preprocessing Train Component")
    {
        when 
        {
            changeset "preprocessing_train/*"
        }
        steps
        {
            container("kaniko")
            {
                script
                {
                    sh '''/kaniko/executor --dockerfile preprocessing_train/Dockerfile \
                                        --context s3://wafer-image-contexts/" \
                                        --destination=aws_account_id.dkr.ecr.region.amazonaws.com/my-repository:${BUILD_NUMBER}"
            '''
                }
            }
        }
    }

    stage("Build and Push Raw Pred Data Validation Component")
    {
        when 
        {
            changeset "raw_pred_dat_validation/*"
        }
        steps
        {
            container("kaniko")
            {
                script
                {
                    sh '''/kaniko/executor --dockerfile raw_pred_data_validation/Dockerfile \
                                        --context s3://wafer-image-contexts/" \
                                        --destination=aws_account_id.dkr.ecr.region.amazonaws.com/my-repository:${BUILD_NUMBER}"
            '''
                }
            }
        }
    }

    stage("Build and Push Raw Train Data Validation Component")
    {
        when 
        {
            changeset "raw_train_data_validation/*"
        }
        steps
        {
            container("kaniko")
            {
                script
                {
                    sh '''/kaniko/executor --dockerfile raw_train_data_validation/Dockerfile \
                                        --context s3://wafer-image-contexts/" \
                                        --destination=aws_account_id.dkr.ecr.region.amazonaws.com/my-repository:${BUILD_NUMBER}"
            '''
                }
            }
        }
    }

    stage("Update Infrastructure Component")
    {
        when 
        {
            changeset "infrastructure/*"
        }
        steps
        {
            sh "curl -fsSL https://get.pulumi.com | sh"
            sh "$HOME/.pulumi/bin/pulumi version"

            nodejs(nodeJSInstallationName: "node 8.9.4") {
                    withEnv(["PATH+PULUMI=$HOME/.pulumi/bin"]) {
                        sh "cd infrastructure && npm install"
                        sh "pulumi stack select ${PULUMI_STACK} --cwd infrastructure/"
                        sh "pulumi up --yes --cwd infrastructure/"
                    }


        }
    }
  }
}