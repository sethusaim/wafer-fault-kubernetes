# Wafer Fault Prediction AWS Microservices System

This is an end to end machine learning system for predicting the failure of the wafer sensors based on the training data. This entire solution is built using AWS Services like AWS S3 buckets (for storing the data), AWS Elastic Container Registry (for storing the container images), and AWS Elastic Kubernetes Service (for running the container image). Apart from AWS services, MLFlow was used for experiment tracking and model versioning and model staging with artifacts stored in AWS S3 bucket. Docker for containerization of application. Jenkins was used for CI builds. ArgoCD for CD deployments. Tekton pipelines for pipeline orchestration. Terraform for managing infrastructure as code. Flask as web server.MongoDB for data storage.

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
The solution application is exposed as API using Flask and application is dockerized using Docker. MLFlow setup is done in an AWS EC2 instance . CI-CD pipeline is created which will deploy the application to AWS Elastic Kubernetes Service, whenever new code is commmited to GitHub.

#### Technologies Used 
- Python
- Sklearn for machine learning algorithms
- Flask for creating an web application
- Machine Learning
- MLFlow for experiment tracking,model versioning and model staging.
- Tekton is used for pipeline orchestration.
- SQL-Lite as backend store for MLFlow server
- AWS EC2 instances for deploying the MLFlow server
- AWS EC2 instances for deploying Jenkins Server
- AWS S3 buckets for data storage, feature store and artifacts store
- MongoDB Atlas for database operations
- AWS ECR for storing the container images
- AWS EKS cluster for managing the microservices
- Docker is used for container builds
- Infrastructure is managed by using terraform  
- Jenkins is used as CI tool 
- Argo CD for continuous delivery tool

### Algorithms Used 
- Random Forest Classifier Model
- XGBoost Classifier Model

### Metrics 
- Accuracy
- ROC AUC score

### Cloud Deployment 
- CI-CD deployment to AWS EKS cluster using Jenkins and ArgoCD using GitOps Principles

## Project Workflow
To create machine learning workflow in microservices architecture, we need understand how microservices in non-AI projects are used. In 
traditional microservices, every single component is created a service and deployed in kubernetes cluster for a choice. Generally,these 
services are owned by small containers over well defined APIs which communicate with each other and information is shared.

Now the question comes, how to implement the same architecture of ML workflows ??.

To address the question we need to understand what all components does our ML workflow contains, for simplicity let us say we have data transformation component,preprocessing component, model training, etc. These components are essential to any ML workflow, but they do not have to be constantly up and running, as in traditional microservices like Web Application Microservices. ML Microservices are kind of different from other microservices, like there intented to some task, when a specific main task is triggered. Like for example, when I want to train my models based on new data, a series of microservices have be triggered, which will internally performed thier tasks and then reach the completion state. 

So how to create ML microservices in the way similar to ML workflow ?

This problem can be approached by creating by microservices to be service independent and stage dependent. The approach is simple, like each task, like let's say raw data validation component is independent from data transformation component, but the data transformation should execute after raw data validation only. So in order to achieve this each component is created as container service and for sequential execution we are using Tekton Pipelines, which is pipeline orchestrator running on kubernetes cluster. 

Now the question comes, how to pass data between independent services, like dataframes and other data ?

To approach this problem, we can store each container artifacts in S3 buckets, and then next container will reference it to that container.
Like the output of one container will be input of other container, thereby maintaining service independency and stage dependency in tekton pipelines. 

Once the tekton pipelines are set up, we have to create the CI pipeline, in which all the components are automatically built and pushed to container registry. For the CI pipeline builds, we are using Jenkins to automate our build process.

Now the question comes why Jenkins ?
Since we are working with microservices architecture, there is high possiblity that not all microservices are updated continuously, like there might be update in Database operation, ie database change from MongoDB to Cassandra just for example. When we commit these changes to the main branch, we want only database service to be updated, it is not neccessary that other services have to be updated, there might be a change or not. But traditional CI tools, the image is built when new code is merged to the main branch. This results in unnessacary image builds, and same images with same content are stored. We do not want that to happen. Jenkins allows us to execute conditional builds in our CI pipeline, like whenever there is code change in data trasformation train folder (We are keeping container services in folders) we shall trigger the build pipeline and updated container image with new tag and content. This results in efficient builds and reduces costs also.

Coming to the pipeline orchestrator, we are using tekton pipelines the reason being simple it is easy to use and we define our pipelines, in the most easiest way, and train and prediction pipelines are triggered when the user tells the application to do perform training or prediction. But, in the CD pipeline when ArgoCD detects changes the git repo, it automatically deploys the microservices to k8s cluster, this approach is good for dependent microservices like web microservices, not ml microservices where microservices are tasks to the main train or prediction pipeline, which are intended to run when triggered to do so. 

So how to deploy ml microservices, and achieve automation in deployment ?

To solve this issue we need to understand the kubernetes control plane functionality, it is designed in such as way that it makes sure that desired state of pod, service or any kubernetes object state is maintained no matter what happens. This is not so usefull to use, the solution is to deploy a static kubernetes pod in the cluster. But after searching the internet, I came to a conclusion that kubernetes cannot be made static. 

But that is when tekton pipelines come to play. Tekton pipelines are similar to other workflow orchestrators like Argo Workflows, KubeFlow, Airflow, etc. Setting up kubeflow and working the kubeflow is challenging, I have tried that concluded that it is feasible for the use case, by default we need a big cluster of atleast 12GB RAM and 50GB memory, now that might be small of big companies who have a lot of data. But the POC, we do not need that much big cluster. Argo Workflows could not work in EKS cluster, and kubeflow interrnally uses argo workflows only. Airflow was not designed for kubernetes, but can be explored.

Tekton pipelines are designed in such a way that each microservice can be defined as task, and group of tasks are called pipeline. This is common in other workflow orchestrators also, but the catch is when the workflow is deployed it automatically starts running, and we do not want to do that, and violates our preset condition. With tekton pipelines, there are two pipeline resources, pne is pipeline and pipelinerun, the difference is simple pipeline is a static kubernetes object and pipelinerun is the kubernetes object which references the pipeline object and then runs it. That means we can control our deployments through conditions, similar to our requirements.

In the git repository, we store the pipeline yaml and not the pipelinerun yaml, so that ArgoCD can deploy the pipeline yaml, and our pipeline stays in kubernetes cluster waiting to be running. Using the tekton cli we can run pipelines whenever we want.

CD pipeline follows GitOps principles and running our services on kubernetes we can use ArgoCD for CD pipeline, it makes our work easier by defining the application state in our git repository. ArgoCD looks for changes in the git repository periodically and reflects the changes automatically. 

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

Before we proceed create a key pair in aws console by which you will connect to the EC2 instance

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

Now that Jenkins is setup in this EC2 instance use public ip of the EC2 instance with port 8080, and click enter. (public_ip:8080)

On successfull login, we shall see jenkins should be unlocked using the initial password which can accessed using 

```bash
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

Copy the password and login to Jenkins server. Next click on the install suggested plugins and wait for installation to complete. Create a username and password for jenkins authentication.

Finally you can access the Jenkins Dashboard in EC2 instance.

Before we configure Jenkins for our usage, we have install awscli,docker and terraform in EC2 instance

#### Install Docker
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

#### Install AWS CLI
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
Restart the instance to make sure that the changes are reflected.

Now we have to configure our aws creds to Jenkins for image builds and push to AWS ECR.

For that click on Manage Jenkins, and then Manage Credentials and then Jenkins and Global credentials and add credentials and select type as secret text and add AWS AWS_ACCESS_KEY_ID and repeat the same for other credentials

For GitHub creds, select type as username with password, with username as your_repo_user_name and id as github and password as Github token. 
To generate the github token, go to your github account and under profile, click settings under that click developer settings, next personal access token, click generate personal access token. Give a token id as Jenkins and scopes to be repo,admin:repo_hook and notifications, next click on generate token and then copy the token and put it in jenkins.

### Creating Build image and update manifest jobs in Jenkins
For running builds in Jenkins, we have to create a pipeline job in jenkins which will get the Jenkinsfile from GitHub and run builds. For that click on new item, give item name buildimage and select pipeline then ok. Next go to pipeline definition select pipeline script from scm and select scm as git and give CI repo url and rename branch from master to main. This sets main Jenkins pipeline which will detect code changes and build image. 

Now we have to update manifest jobs CD pipeline, for that we shall go to dashboard and click on new item and give item name as updatemanifest and select pipeline and click ok then select "This project is parameterized" and add string parameter. and start giving string parameters like DOCKERTAG with default as latest, REPO_NAME with default as test, COMP_FILE with default as test.yaml. In pipeline definition, select pipeline script from SCM and select scm as git and give repo url of CD repo with branch as main.

### Setup GitHub Webhook trigger for Jenkins for automatic CI builds
For github hook, we need to get the url of jenkins instance and go to the CI repository and then click on settings and select webhook and add webhook and in payload url give the value as http://public_ip:8080/github-webhook/ (put your own public ip) and content type as application/json and select just the push event and click on add webhook.Now go to jenkins buildimage job and click configure and under build triggers select Github hook triggers for Gitscm polling and save.

### Application setup in EC2 instance
The application microservice is the important part of the project because it controls the train and prediction pipelines running in our cluster. To make things simplier, we are deploying the application microservice in the kubernetes master control which we have setup for controlling the cluster. 

We shall require kubernetes config file for controlling the cluster, tekton cli to run pipelines, docker to run application microservice

EKS cluster provisioning takes around 13min to 15min. After the provisioning of the EKS cluster along 3 node groups.Execute the following commands to add kubeconfig to application instance

#### Launch the application instance
Open code editor in infrastructure folder and execute the following commands.

```bash
terraform init
```

```bash
terraform apply -target=module.application_instance
```

#### Updating the kubeconfig file
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
On prompt give your aws creds with default output as json. Once the install kubectl in EC2 instance

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
This means that kubeconfig of cluster is updated in EC2 instance and can be accessed from EC2 instance as a master node.

#### Installing Tekton CLI
```bash
sudo apt update
```

```bash
sudo apt install -y gnupg
```

```bash
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 3EFE0E0A2F2F60AA
```

```bash
echo "deb http://ppa.launchpad.net/tektoncd/cli/ubuntu eoan main"|sudo tee /etc/apt/sources.list.d/tektoncd-ubuntu-cli.list
```

```bash
sudo apt update && sudo apt install -y tektoncd-cli
```

These commands install the tekton cli, to verify the installation execute

```bash
tkn version
```

### Setup application as service 
We need to run the application in the EC2 instance continuously without us running the start or stop commands. So, how do we achieve this ?
The approach is simple we need to run the application as service inside EC2 instance. In order to do so we need perform some operations and the commands to do so are

```bash
sudo apt update
```

```bash
sudo apt-get update
```

```bash
sudo apt install python3-pip -y
```

```bash
git init 
```

```bash
git remote add origin https://github.com/sethusaim/Wafer-Fault-Kubernetes.git
```

Replace my repo url with your repo url

```bash
git fetch origin
```

```bash
git checkout origin/main -- application
```

```bash
cd application
```

```bash
pip3 install -r requirements.txt
```

On installation of flask, you will get PATH warning, to prevent that add flask to PATH

```bash
cd /home/ubuntu/.local/bin
```

```bash
sudo mv flask /usr/bin
```

```bash
cd /home/ubuntu
```

```bash
sudo apt-get install nginx -y
```

```bash
pip3 install gunicorn
```
or use

```bash
sudo apt install gunicorn
```

For authentication of web server
```bash
sudo apt-get install -y apache2-utils
```

You will be prompted to give password for USERNAME, input them and remember it for accessing the webserver
```bash
sudo htpasswd -c /etc/nginx/.htpasswd USERNAME
```

```bash
cd /etc/nginx/sites-enabled
```

```bash
sudo nano flaskapp
```

NGINX server configuration for authentication
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
```bash
sudo service nginx restart
```
On successfull setup, nginx will restart without any errors

```bash
cd /home/ubuntu/
```

Creating the application as service

```bash
cd  /etc/systemd/system
```

```bash
sudo nano app.service
```

```bash
[Unit]
Description=Application Service
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/application
Restart=on-failure
RestartSec=30

ExecStart=/usr/bin/gunicorn3 --workers 3 --bind unix:flaskapp.sock -m 007 app:app

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
```

```bash
sudo systemctl enable app
```

```bash
sudo systemctl enable app
```

```bash
sudo systemctl start app
```
Now that the application service is created, we need to tell nginx that use that flaskapp.sock file. Before we do that lets check if flaskapp.sock file is created or not

```bash
cd /home/ubuntu/application
```

In this directory we shall see that flaskapp.sock file is created and can be used. Coming to the nginx configuration, execute these commands

```bash
cd /etc/nginx/sites-enabled/
```

```bash
sudo nano app
```

```bash
server {
    listen 8080;
    server_name YOUR_IP_OR_DOMAIN;
    auth_basic “Administrator-Area”;
    auth_basic_user_file /etc/nginx/.htpasswd; 

    location / {
        proxy_pass http://unix:/home/ubuntu/application/flaskapp.sock;
        include /etc/nginx/proxy_params;
        proxy_redirect off;
    }
}
```
Replace the server configuration or edit the file accordingly

```bash
cd /home/ubuntu
```

```bash
sudo service nginx restart
```

```bash
sudo service app restart
```

On successfull restart of app and nginx, we can access the application on ec2 public ip with port as 8080, and that is it. Our application is set up as service in EC2 instance

### How to perform CI CD for application microservice ??
Now that the previous step we have created our flask app as a service. The question is how to patch any new changes made to application source code. In simple CI CD to flask application running as a service in EC2 instance. Well, the approach is very simple, we shall use Jenkins and Git to do so, the workflow is fairly simple, first new application code is merged to main branch, on the commiting to the main branch, Jenkins will perform a series of steps which include connecting to the EC2 instance and getting the application_cicd.sh bash file from the repo and executing it. The bash file consists of commands wchich will get the source from Github, and stops the service and installs requirements.txt file and restarts nginx and application service, and that is it we are able to achieve CI CD for application service running in the ec2 instance, since Jenkins runs this stage when there is application code change. 

One thing to note that the filename "app.py" should be same, else the application might not work, since the initial setup was done using application "app.py" as filename. If we want change that to something else, make the neccessary changes to app.service file

### MLFlow setup in EC2 instance
For setting up mlflow in EC2 instance, open your code editor in the infrastructure folder and uncomment the mlflow_instance module, and then execute the following commands,

```bash
terraform init
```

```bash
terraform apply
```
These commands will launch, t2.small instance with neccessary security groups. After some time, the mlflow instance will be up and running. Connect to the EC2 instance using key pair. On successfull login, execute the following commands,

```bash
sudo apt update
```

```bash
sudo apt-get update
```

#### Install Anaconda in EC2 instance and create a env for mlflow
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
Now close the connection made via ssh and reconnect via ssh to see the changes in EC2 instance, we can see that deafult env is to set bsse which indicates that anaconda is successfully installed.

#### Create MLFLow as service in EC2 instance
Now that anaconda is setup in EC2 instance, we shall create a conda env named mlflow and install the required packages. In order to do that execute the following commands.

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

##### Expose mlflow server as a service in EC2 instance
Now we have to expose mlflow server as a service in EC2 instance. In order to do so, execute the following commands

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
If these commands do not return any error that means mlflow service is setup in EC2 instance, and can be accessed via public ip on ports 8000 or 8080. Go to the browser, and paste PUBLIC_IP:8080 or PUBLIC_IP:8000.

If everything is done properly, we should then see the mlflow dashboard in our browser.Sometimes, you might be prompted to give your username and password for login, remember that username and password is the same which have configured for nginx. The public ip with port, mlflow username and mlflow password acts as a environment variables when using model training service. 

### EKS cluster setup
Since we are using microservices architecture, kubernetes plays an important role in microservices architecture by orchestrating and managing our containters/microservices in the cloud. In AWS cloud, there is managed serviced called Elastic Kubernetes Service which allows us to create kubernetes cluster on AWS cloud. In order to create a kubernetes, open code editor in infrastructure folder, and uncomment two modules one is eks_cluster and kube_master modules. The main purpose kube_master module, to control the kubernetes cluster from an EC2 instance and not from local machine. 

To create a kubernetes cluster, we have to execute the following commands,

```bash
terraform init
```

```bash
terraform apply 
```
These commands will be initialize the backend required to run terraform and stores the state in s3 bucket. The terraform module includes the launch of 5 instances which are of type t2.medium, which approximately 20GB cluster node groups. 

Now you might be why that much big cluster ??. The answer is we need to setup tekton, ArgoCD and on top of that we need to run our microservices. So approximately we need might 20GB cluster. We can scale up and down by changing the cluster configuration in terraform files or by using autoscaler, or completely shift to serverless infrastructure. That option is left to end user itself. I have choosen provisioned cluster of 20GB which should be enough to run our applications.

### Tekton Setup
Since we are using tekton for pipeline orchestration, we need to setup tekton in eks cluster. tekton pipelines can be set up in eks cluster, by looking in the docuementation of Tekton. The setup can be done by executing the following commands

#### Installing Tekton pipelines

```bash
kubectl apply --filename https://storage.googleapis.com/tekton-releases/pipeline/latest/release.yaml
```

```bash
kubectl get pods --namespace tekton-pipelines --watch
```
Once the pods reach running state, exit from watch mode.

#### Accessing Tekton Dashboard

```bash
kubectl apply --filename https://github.com/tektoncd/dashboard/releases/latest/download/tekton-dashboard-release.yaml
```

```bash
kubectl get pods --namespace tekton-pipelines --watch
```

Once the pods reached running state exit from watch mode. By default tekton-dashboard service will be of type ClusterIP, but in order to access it via browser, we need to setup LoadBalancer service, which can be achieved by executing the following commands.

```bash
kubectl patch svc tekton-dashboard -n tekton-pipelines -p '{"spec":{"type":"LoadBalancer"}}'
```

After a few minutes, load balancer will be provisioned, and tekton dashboard can be accessed through the loadbalancer ip on port 9097. To get the load balancer ip address 

```bash
kubectl -n tekton-pipelines get svc tekton-dashboard
```

Copy the external loadbalancer ip address and paste it in the browser on successfully installation, you will be able to see the tekton dashboard in the browser. 

### ArgoCD setup
Argo CD is a declarative, GitOps continuous delivery tool for Kubernetes.Application definitions, configurations, and environments should be declarative and version controlled. Application deployment and lifecycle management should be automated, auditable, and easy to understand.

To setup ArgoCD in EKS cluster, execute the following steps, 

```bash
kubectl create namespace argocd
```

```bash
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

```bash
kubectl -n argocd get pods --watch
```
Once all the pods are in running state, exit from watch mode.

```bash
kubectl -n argocd get svc
```
By default, the argocd-server service is of type ClusterIP, we need to patch a load balancer to access it externally.

```bash
kubectl patch svc argocd-server -n argocd -p '{"spec": {"type": "LoadBalancer"}}'
```
After few minutes load balancer get provisioned, access the load balancer ip by executing 

```bash
kubectl -n argocd get svc argocd-server
```
On successfull installation, we shall be able to see the login page of ArgoCD server, the initial username is admin and password can get retrived through executing this command

```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo
```

Create a new namespace for tekton pipelines to run
```bash
kubectl create ns wafer
```

#### Install the ArgoCD CLI

```bash
wget https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64
```

```bash
chmod +x argocd-linux-amd64
```

```bash
sudo mv argocd-linux-amd64 /usr/local/bin/argocd
```

On successfull login we shall be able to access the ArgoCD dashboard. Now come to terminal and execute the following command

```bash
argocd login <ARGOCD_SERVER>
```
type "y" for insecure login, it is insecure because it runs on https. give username as admin and password retrived from running command

```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo
```

Now we shall change the initial password to our own password, execute these commands

```bash
argocd account update-password
```
Give the initial password and new password, the username will be "admin". Now if we go the dashboard, we see that we have been logged out. Login again with the username as "admin" and password as the updated password. On successfull login, you shall be see that ArgoCD dashboard again.

Now that ArgoCD is setup in EKS cluster, we have to tell ArgoCD will repository to monitor, and which resources to deploy. In order to do that go to dashboard, click on create application.

Give any application name, it does not matter. Project to be default. Sync policy to be automatic. In the repository url give the url of the CD repository and path needs to be "./components" since our manifest files are stored in components folder. 

In the cluster url, select default cluster we can use argocd to deploy to other cluster also. In the namespace section select the namespaces which was created to run tekton pipelines, and click on create and thats it ArgoCD now monitors the CD repo every 3 minutes to sync if they are any new changes in the git repo.

### Destroy everything and clean up the resources in cloud
Now that everthing is tested out and successfully executed, we destroy the resources created so that we do not incur more charges from AWS cloud. In order to do that run

Before we destroy everthing, we have to EC2 dashboard and in there go to load balancers and delete the load balancers, because since the load balancer is managed by terraform it becomes difficult for terraform to destroy it. 

Also, empty the data present s3 buckets, if you want them make a backup of it and then empty them. Once these things are done execute

```bash
terraform destroy --auto-approve
```

Sometimes even after deleting the load balancers, terraform takes time to delete the wafer resource, if that is the case stop the destroy and manually delete the vpc from vpc dashboard

That is all from my side regarding this project. Thank you and hope you learnt from it.
Feel free to contact me at sethusaim@gmail.com regarding any clarifactions or doubts regarding the project.