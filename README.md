# Wafer Fault Prediction AWS System

This is an end to end machine learning system for predicting the failure of the wafer sensors based on the training data. This entire solution is built using AWS Services like AWS S3 buckets (for storing the data), AWS DynamoDB (for logging and improvising the system performance), AWS Elastic Container Registry (for storing the container images), and AWS Elastic Container Service (for running the container image). Apart from AWS services, MLFlow was used for experiment tracking and model versioning and model staging with artifacts stored in AWS S3 bucket. Docker for containerization of application. 

### Problem Statement 
To build a classification methodology to predict the failure of wafer sensors on the basis of given training data. 

### Approach to building the solution
In the first place, whenever we start a machine learning project, we need to sign a data sharing agreement with the client, where sign off some of the parameters like,

    1. Format of data - like csv format or json format,etc
    2. Number of Columns
    3. Length of date stamp in the file
    4. Length of time stamp in the file
    5. DataType of each sensor - like float,int,string

Once the data sharing agreement,is created we create a master data management, which is nothing but the schema_training.json and schema_prediction.json file. Using this data we shall validate the batch data which is sent to us. 

The data which is sent to us will be stored in AWS S3 buckets. From AWS S3 buckets, using schema file, the data is validated againist filename, column length, and missing values in the column. 

Once the data validation is done, the data transformation pipeline is triggered, where we add quotes to string values in the data.After the data transformation is done, The good data is stored is stored in MongoDB and once is stored in database, we will export a csv file which will be used training for the models.

The model training is done by using a customized machine learning approach,in which the entire training data is divided to clusters using KMeans algorithm, and for every cluster of data, a model is trained and then model is used for prediction. So before we apply a clustering algorithm to the data, we need to preprocess the data as done in the jupyter notebook like  missing values, replacing invalid values. Then elbow plot is created and number of clusters is created and based on the number of clusters XGBoost model and Random Forest Model are trained
are saved in AWS S3 buckets.

Once the models are trained,they are tested againist the test data and model score is found out.Now MLFlow is used for logging the parameters,metrics and models to the server. Once the logging of parameters,metrics and models is done. A load production model is triggered to which will get the top models based on metrics and then transitioned to production or staging depending on the condition.

### Post Model Training
The solution application is exposed as API using FastAPI and application is dockerized using Docker. MLFlow setup is done in an AWS EC2 instance . CI-CD pipeline is created which will deploy the application to AWS Elastic Container Service, whenever new code is commmited to GitHub.

#### Technologies Used 
- Python
- Sklearn for machine learning algorithms
- FastAPI for creating an web application
- Machine Learning
- MLFlow for experiment tracking,model versioning and model staging.
- Kubeflow is used for pipeline orchestration.
- SQL-Lite as backend store for MLFlow server
- AWS EC2 instances for deploying the MLFlow server
- AWS S3 buckets for data storage
- MongoDB Atlas for database operations
- Docker Registry for storing the container images
- AWS EKS cluster for managing the container
- Podman is used for container builds 
- Jenkins is used as CI tool 
- Argo CD for continuous delivery tool

### Algorithms Used 
- Random Forest Classifier Model
- XGBoost Classifier Model

### Metrics 
- Accuracy
- ROC AUC score

### Cloud Deployment 
- CI-CD deployment to AWS EKS cluster using Jenkins and ArgoCD

## Project Workflow
To create machine learning workflow in microservices architecture, we need understand how microservices in non-AI projects are used. In 
traditional microservices, every single component is created a service and deployed in kubernetes cluster for a choice. Generally,these 
services are owned by small containers over well defined APIs which communicate with each other and information is shared.

Now the question comes, how to implement the same architecture of ML workflows ??.

To address the question we need to understand what all components does our ML workflow contains, for simplicity let us say we have data transformation component,preprocessing component, model training, etc. These components are essential to any ML workflow, but they do not have to be constantly up and running, as in traditional microservices like Web Application Microservices. ML Microservices are kind of different from other microservices, like there intented to some task, when a specific main task is triggered. Like for example, when I want to train my models based on new data, a series of microservices have be triggered, which will internally performed thier tasks and then reach the completion state. 

So how to create ML microservices in the way similar to ML workflow ?

This problem can be approached by creating by microservices to be service independent and stage dependent. The approach is simple, like each task, like let's say raw data validation component is independent from data transformation component, but the data transformation should execute after raw data validation only. So in order to achieve this each component is created as container service and for sequential execution we are using Kubeflow Pipelines, which is pipeline orchestrator running on kubernetes cluster. 

Now the question comes, how to pass data between independent services, like dataframes and other data ?

To approach this problem, we can store each container artifacts in S3 buckets, and then next container will reference it to that container.
Like the output of one container will be input of other container, thereby maintaining service independency and stage dependency in kubeflow pipelines. 

Once the kubeflow pipelines are set up, we have to create the CI pipeline, in which all the components are automatically built and pushed to container registry. For the CI pipeline builds, we are using Jenkins to automate our build process.

Now the question comes why Jenkins ?
Since we are working with microservices architecture, there is high possiblity that not all microservices are updated continuously, like there might be update in Database operation, ie database change from MongoDB to Cassandra just for example. When we commit these changes to the main branch, we want only database service to be updated, it is not neccessary that other services have to be updated, there might be a change or not. But traditional CI tools, the image is built when new code is merged to the main branch. This results in unnessacary image builds, and same images with same content are stored. We do not want that to happen. Jenkins allows us to execute conditional builds in our CI pipeline, like whenever there is code change in data trasformation train folder (We are keeping container services in folders) we shall trigger the build pipeline and updated container image with new tag and content. This results in efficient builds and reduces costs also.

Coming to the pipeline orchestrator, we are using kubeflow pipelines the reason being simple it is easy to use and we define our custom pipelines with conditions and the way we want to run our pipelines like DAG workflows, without worrying about the underlying kubernetes yaml.

CD pipeline follows GitOps principles and running our services on kubernetes we can use ArgoCD for CD pipeline, it makes our work easier by defining the application state in our git repository. ArgoCD looks for changes in the git repository periodically and reflects the changes automatically. 

Now the question comes how to manange other components which are running on kubeflow pipelines, since in kubeflow pipelines we do not have to write kind of kubernetes yaml file ?

Yes, it is true that kubeflow pipelines do not require us to write any kubernetes yaml file, but kubeflow expects us to write our services in the form of very simple yaml file defining container image name and image run command. We can update these yaml files in our CI pipeline and upload them CD git repository. But the problem is ArgoCD only looks for kubernetes yaml. So in order to resolve this and still follow GitOps principles, we can use a GitHub actions which will sync our files present in git repository to s3 buckets and loaded be for kubeflow pipelines to be executed based on route passed to application service.

The same approach is followed for prediction pipeline also.

For creating and managing the infrastructure, we are using terraform intergrated with Jenkins for GitOps type infrastructure provising and maintainence. 

## How to Setup the Project
Since we are following GitOps principles and Microservices architecture to solve the problem statement. Initially we have to create two repositories in GitHub, one for CI pipeline and other for CD pipeline.

Once the repositories are created, in the CI repository, clone this repository using this command

```bash 
git clone https://github.com/sethusaim/Wafer-Fault-Kubernetes.git
```

### Jenkins Setup in EC2 instance
Previously install terraform in your local machine, be Linux,Mac or Windows. https://www.terraform.io/downloads

Install AWS CLI

```bash
pip install awscli
```
Configure aws creds

```bash
aws configure
```

Open your code editor in the infrastructure folder. In module.tf file comment all modules expect jenkins instance and execute the following commands.

Before we proceed create a key pair in aws console by which you will connect to the ec2 instance

Make sure to change the key pair name from sethu (which is mine) to your own key pair name.

Then execute this command, which will initialize all backend required by terraform to function

```bash
terraform init 
```

This command applies the uncommented modules which are required by us 

```bash
terraform apply
```
Once the instance provisioning is done, SSH into the instance using any SSH tool like Putty, Mobaxterm,etc and execute the following commands

```bash
sudo apt update
```
```bash
sudo apt-get update
```

Add Repository Key
```bash
wget -q -O - https://pkg.jenkins.io/debian-stable/jenkins.io.key | sudo apt-key add -
```

Add Package Repository
```bash
sudo sh -c 'echo deb http://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'
```

```bash
sudo apt update
```

Install Jenkins Dependencies
```bash
sudo apt install openjdk-8-jre -y
```

```bash
sudo apt install jenkins -y
```

Enable the Jenkins service to start at boot:
```bash
sudo systemctl enable jenkins
```

Start Jenkins as a service
```bash
sudo systemctl start jenkins
```

You can check the status of the Jenkins service using the command
```bash
sudo systemctl status jenkins
```

Now that Jenkins is setup in this ec2 instance use public ip of the ec2 instance with port 8080, and click enter. (public_ip:8080)

On successfull login, we shall see jenkins should be unlocked using the initial password which can accessed using 

```bash
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

Copy the password and login to Jenkins server. Next click on the install suggested plugins and wait for installation to complete. Create a username and password for jenkins authentication.

Finally you can access the Jenkins Dashboard in ec2 instance.

Before we configure Jenkins for our usage, we have install awscli,docker and terraform in ec2 instance

Install Docker
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
```

```bash
sudo sh get-docker.sh
```

```bash
sudo groupadd docker
```

```bash
sudo usermod -aG docker $USER
```

```bash
sudo usermod -aG docker jenkins
```

```bash
newgrp docker
```

Install AWS cli
```bash
sudo apt install awscli
```

Install Terraform 

```bash
sudo apt-get update && sudo apt-get install -y gnupg software-properties-common curl
```

```bash
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
```

```bash
sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
```

```bash
sudo apt-get update && sudo apt-get install terraform
```

Now we have to configure our aws creds to Jenkins for image builds and push to AWS ECR.

For that click on Manage Jenkins, and then Manage Credentials and then Jenkins and Global credentials and add credentials and select type as secret text and add AWS AWS_ACCESS_KEY_ID and repeat the same for other credentials

For GitHub creds, select type as username with password, with username as your_repo_user_name and id as github and password as Github token. 
To generate the github token, go to your github account and under profile, click settings under that click developer settings, next personal access token, click generate personal access token. Give a token id as Jenkins and scopes to be repo,admin:repo_hook and notifications, next click on generate token and then copy the token and put it in jenkins.

### Creating Build image and update manifest jobs in Jenkins
For running builds in Jenkins, we have to create a pipeline job in jenkins which will get the Jenkinsfile from GitHub and run builds. For that click on new item, give item name buildimage and select pipeline then ok. Next go to pipeline definition select pipeline script from scm and select scm as git and give CI repo url and rename branch from master to main. This sets main Jenkins pipeline which will detect code changes and build image. 

Now we have to update manifest jobs CD pipeline, for that we shall go to dashboard and click on new item and give item name as updatemanifest and select pipeline and click ok then select "This project is parameterized" and add string parameter. and start giving string parameters like DOCKERTAG with default as latest, REPO_NAME with default as test, COMP_FILE with default as test.yaml. In pipeline definition, select pipeline script from SCM and select scm as git and give repo url of CD repo with branch as main.