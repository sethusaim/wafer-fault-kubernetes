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

### Setup GitHub Webhook trigger for Jenkins for automatic CI builds
For github hook, we need to get the url of jenkins instance and go to the CI repository and then click on settings and select webhook and add webhook and in payload url give the value as http://public_ip:8080/github-webhook/ (put your own public ip) and content type as application/json and select just the push event and click on add webhook.Now go to jenkins buildimage job and click configure and under build triggers select Github hook triggers for Gitscm polling and save.

### MLFlow setup in EC2 instance
For setting up mlflow in ec2 instance, open your code editor in the infrastructure folder and uncomment the mlflow_instance module, and then execute the following commands,

```bash
terraform init
```

```bash
terraform apply
```
These commands will launch, t2.small instance with neccessary security groups. After some time, the mlflow instance will be up and running. Connect to the ec2 instance using key pair. On successfull login, execute the following commands,

```bash
sudo apt update
```

```bash
sudo apt-get update
```

#### Install Anaconda in ec2 instance and create a env for mlflow
```bash
wget https://repo.anaconda.com/archive/Anaconda3-2022.05-Linux-x86_64.sh
```

```bash
bash Anaconda3-2022.05-Linux-x86_64.sh
```
When prompted type yes and press enter to confirm the location of anaconda3. This process might take a few minutes of time. Once done execute the following commands.

```bash
export PATH=~/anaconda3/bin:$PATH
```

```bash
conda init bash
```
Now close the connection made via ssh and reconnect via ssh to see the changes in ec2 instance, we can see that deafult env is to set bsse which indicates that anaconda is successfully installed.

#### Create MLFLow as service in ec2 instance
Now that anaconda is setup in ec2 instance, we shall create a conda env named mlflow and install the required packages. In order to do that execute the following commands.

```bash
conda create -n mlflow python=3.7.6 -y
```

```bash
conda activate mlflow
```

```bash
pip3 install mlflow
```

```bash
sudo apt install -y nginx 
```

```bash
sudo apt-get install -y apache2-utils
```

```bash
cd /etc/nginx/sites-enabled
```

This command lets you create user profile for mlflow authentication, replace USERNAME with your username,(do remember it or keep a note of it since we will be requiring it for model training service). Once the command is executed, it prompts you to give a new password, fill the details (remember the password or make note of it, we will be requiring it for model training service).  
```bash
sudo htpasswd -c /etc/nginx/.htpasswd USERNAME
```

Now that the username and password are created, we have to create a mlflow nginx configuration file, to tell nginx to listen to our public ip, with our username and password details, like a nginx reverse proxy for HTTP authentication for API calls made by user to MLFlow server. In order to do that, execute the following commands

```bash
sudo nano mlflow
```
```bash
server {
    listen 8080;
    server_name YOUR_IP_OR_DOMAIN;
    auth_basic “Administrator-Area”;
    auth_basic_user_file /etc/nginx/.htpasswd; 

    location / {
        proxy_pass http://localhost:8000;
        include /etc/nginx/proxy_params;
        proxy_redirect off;
    }
}
```
We have successfully created mlflow nginx configuration file. Now we have apply those changes, in order to do so, execute the following commands

```bash
sudo service nginx start
```
If above command does not return any error, it means that you have successfully configured nginx. 

##### Expose mlflow server as a service in ec2 instance
Now we have to expose mlflow server as a service in ec2 instance. In order to do so, execute the following commands

```bash
cd /home/ubuntu
```

```bash
cd  /etc/systemd/system
```

```bash
sudo nano mlflow-tracking.service
```

```bash
[Unit]
Description=MLflow tracking server
After=network.target

[Service]
Restart=on-failure
RestartSec=30

ExecStart=/bin/bash -c 'PATH=/home/ubuntu/anaconda3/envs/CREATED_ENV/bin/:$PATH exec mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root s3://WAFER_MLFLOW_BUCKET_NAME/ --host 0.0.0.0 -p 8000'

[Install]
WantedBy=multi-user.target
```

Now that we have added a service file for mlflow, we have to reload the daemon and start the mlflow service

```bash
cd /home/ubuntu
```

```bash
sudo systemctl daemon-reload
```

```bash
sudo systemctl enable mlflow-tracking 
```

```bash
sudo systemctl start mlflow-tracking
```
If these commands do not return any error that means mlflow service is setup in ec2 instance, and can be accessed via public ip on ports 8000 or 8080. Go to the browser, and paste PUBLIC_IP:8080 or PUBLIC_IP:8000.

If everything is done properly, we should then see the mlflow dashboard in our browser.Sometimes, you might be prompted to give your username and password for login, remember that username and password is the same which have configured for nginx. The public ip with port, mlflow username and mlflow password acts as a environment variables when using model training service. 

### EKS cluster setup
Since we are using microservices architecture, kubernetes plays an important role in microservices architecture by orchestrating and managing our containters/microservices in the cloud. In AWS cloud, there is managed serviced called Elastic Kubernetes Service which allows us to create kubernetes cluster on AWS cloud. In order to create a kubernetes, open code editor in infrastructure folder, and uncomment two modules one is eks_cluster and kube_master modules. The main purpose kube_master module, to control the kubernetes cluster from an ec2 instance and not from local machine. 

To create a kubernetes cluster, we have to execute the following commands,

```bash
terraform init
```

```bash
terraform apply 
```
These commands will be initialize the backend required to run terraform and stores the state in s3 bucket. The terraform module includes the launch of 5 instances which are of type t2.medium, which approximately 20GB cluster node groups. 

Now you might be why that much big cluster ??. The answer is we need to setup KubeFlow, ArgoCD and on top of that we need to run our microservices. So approximately we need might 20GB cluster. We can scale up and down by changing the cluster configuration in terraform files or by using autoscaler, or completely shift to serverless infrastructure. That option is left to end user itself. I have choosen provisioned cluster of 20GB which should be enough to run our applications.


EKS cluster provisioning takes around 13min to 15min. After the provisioning of the EKS cluster along 5 node groups and Kube master ec2 instance is done. Connect to kube master via ssh and execute the following commands.

```bash
sudo apt update
```

```bash
sudo apt-get update
```

```bash
sudo apt install awscli
```

```bash
aws configure
```
On prompt give your aws creds with default output as json. Once the install kubectl in ec2 instance

```bash
curl -o kubectl https://amazon-eks.s3.us-west-2.amazonaws.com/1.19.6/2021-01-05/bin/linux/amd64/kubectl
```

```bash
chmod +x ./kubectl
```

```bash
sudo mv ./kubectl /usr/local/bin 
```

```bash
kubectl version --short --client
```

```bash
aws eks update-kubeconfig --name EKS_CLUSTER_NAME
```
To check whether kubeconfig is updated or not, run the following commnands, and you shall see that 5 nodes are shown in console

```bash
kubectl get nodes
```
This means that kubeconfig of cluster is updated in ec2 instance and can be accessed from ec2 instance as a master node.

### Kubeflow setup
Since we are using kubeflow for pipeline orchestration, we need to setup kubeflow in eks cluster. Kubeflow can be set up in eks cluster, by looking in the docuementation of Kubeflow on AWS. The setup can be done by executing the following commands

```bash
export KUBEFLOW_RELEASE_VERSION="v1.4.1"
```

```bash
export AWS_RELEASE_VERSION="v1.4.1-aws-b1.0.0"
```

```bash
git clone https://github.com/awslabs/kubeflow-manifests.git && cd kubeflow-manifests
```

```bash
git checkout ${AWS_RELEASE_VERSION}
```

```bash
git clone --branch ${KUBEFLOW_RELEASE_VERSION} https://github.com/kubeflow/manifests.git upstream
```
If you refer the docuementation, we can see that they have given single line command to install kubeflow in eks cluster. Before we proceed we have install kustomize in the ec2 instance and to do so execute the following commands

```bash
sudo apt install snapd
```

```bash
sudo snap install kustomize
```

```bash
while ! kustomize build docs/deployment/vanilla | kubectl apply -f -; do echo "Retrying to apply resources"; sleep 10; done
```

After few minutes, the installation will be completed and kubeflow will be setup in eks cluster. To verify that the kubeflow is running, execute the following command

```bash
kubectl -n kubeflow get all
```
You should see that status of all pods are in running, and kubeflow dashboard can accessed by exposing the service svc/istio-ingressgateway through a load balancer. In order to do so, execute the command

```bash
kubectl patch svc istio-ingressgateway -p '{"spec": {"ports": [{"port": 8080,"targetPort": 8080,"name": "http"}],"type": "LoadBalancer"}}' -n istio-system
```
After few minutes load balancer will be provisoned and kubeflow dashboard can be accessed by getting the loadbalancer address, by executing the command

```bash
kubectl -n istio-system get svc istio-ingressgateway 
```
Copy the external loadbalancer ip address and paste it in the browser and you shall see that dex login page where you have to login with username and password. The default username and password is user@example.com and 12341234. 

On successfully login, you will be able to see the kubeflow dashboard in the browser. Get the loadbalancer url from browser and then export it as environment variable KFP_HOST to access the kubeflow dashboard by using kubeflow pipelines sdk.


### ArgoCD setup