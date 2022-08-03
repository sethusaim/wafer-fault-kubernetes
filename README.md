# Wafer Fault Prediction using AWS Microservices System

This is an end to end machine learning system for predicting the failure of the wafer sensors based on the training data. This entire solution is built using AWS Services like AWS S3 buckets (for storing the data), AWS Elastic Container Registry (for storing the container images), and AWS Elastic Kubernetes Service (for running the container image). Apart from AWS services, MLFlow was used for experiment tracking and model versioning and model staging with artifacts stored in AWS S3 bucket. Docker for containerization of application. Jenkins was used for CI builds. ArgoCD for CD deployments. Tekton pipelines for pipeline orchestration. Terraform for managing infrastructure as code. Flask as web server.MongoDB for data storage.

## Project Practical Demo

- Theory Explanation - https://drive.google.com/file/d/17THCUvwkhVvGS-HlF2bIVh77kmaezjYc/view?usp=sharing

- Practical Implementation - https://drive.google.com/file/d/1Qf2sHB9uBidAPtPSY9AHb-4n3PlTJq4Y/view?usp=sharing [Long Video]

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

Once the data validation is done, the data transformation pipeline is triggered, where we add quotes to string values in the data.After the data transformation is done the good data is stored in MongoDB and then will export a csv file which will be used for model training.

The model training is done by using a customized machine learning approach in which the entire training data is divided into clusters using KMeans algorithm, and for every cluster of data, a model is trained and then used for prediction. So before we apply a clustering algorithm to the data, we need to preprocess the data as done in the jupyter notebook like  imputing missing values, replacing invalid values. Then elbow plot is created and based on the number of clusters XGBoost model and Random Forest Model are trained and saved in AWS S3 buckets.

Once the models are trained,they are tested againist the test data and model score is found out.Now MLFlow is used for logging the parameters,metrics and models to the server. Once this process is completed, a load production model pipeline is triggered, which will get the top models based on metrics and then transition them to production or staging depending on the condition.

### Post Model Training
The solution application is exposed as API using Flask and application is containerized using Docker. MLFlow setup is done in an AWS EC2 instance . CI-CD pipeline is created which will deploy the application to AWS Elastic Kubernetes Service, whenever new code is commmited to GitHub.

#### Technologies Used 
- Python
- Sklearn for machine learning algorithms
- Flask for creating an web application
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
- Ansible is used as configuration management tool
- Prometheus is used for metrics collection
- Grafana is used for metrics visulization
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

Tekton pipelines are designed in such a way that each microservice can be defined as task, and group of tasks are called pipeline. This is common in other workflow orchestrators also, but the catch is when the workflow is deployed it automatically starts running, and we do not want to do that, and violates our preset condition. With tekton pipelines, there are two pipeline resources, one is pipeline and pipelinerun, the difference is simple pipeline is a static kubernetes object and pipelinerun is the kubernetes object which references the pipeline object and then runs it. That means we can control our deployments through conditions, similar to our requirements.

In the git repository, we store the pipeline yaml and not the pipelinerun yaml, so that ArgoCD can deploy the pipeline yaml, and our pipeline stays in kubernetes cluster waiting to be running. Using the tekton cli we can run pipelines whenever we want.

CD pipeline follows GitOps principles and running our services on kubernetes we can use ArgoCD for CD pipeline, it makes our work easier by defining the application state in our git repository. ArgoCD looks for changes in the git repository periodically and reflects the changes automatically. 

For creating and managing the infrastructure, we are using terraform intergrated with Jenkins for GitOps type infrastructure provising and maintainence. 

## How to Setup the Project
Since we are following GitOps principles and Microservices architecture to solve the problem statement. Initially we have to create two repositories in GitHub, one for CI pipeline and other for CD pipeline.

Once the repositories are created, in the CI repository, clone this repository using this command

```bash 
git clone https://github.com/sethusaim/Wafer-Fault-Kubernetes.git
```

### Setup Ansible Server in EC2 instance
First go to aws ec2 console, and click on launch instance type the below configuration

Name - Ansible Server

AMI - Ubuntu 20.04

Instance Type - t2.medium

Key Pair - your_key_pair

Network Setting : ports - 22,9090,9100, source_type - anywhere

After the configuration is done, click on launch instance. Once the instance is up and running. SSH into instance using the selected key using any SSH tools, like Putty, MobaXterm,etc (your choice)

Once the ssh connection is done, run the following commands to setup ansible and other packages in the ansible instance

```bash
wget https://raw.githubusercontent.com/sethusaim/Wafer-Fault-Kubernetes/main/scripts/setup_ansible.sh
```

```bash
bash setup_ansible.sh
```
On successfull execution of the script,we shall see that ansible,terraform,awscli got installed and infrastructure and ansible_playbooks folders are created.

#### Setup AWS credentials
```bash
aws configure
```

#### Setup variables.yml
Run the following and edit the values based on your choice

```bash
sudo nano ansible_playbooks/vars/variables.yml
```

### Jenkins Setup in EC2 instance
First SSH into ansible server run the commands to provision the jenkins instance

```bash
terraform -chdir=infrastructure init
```

```bash
terraform -chdir=infrastructure apply -target=module.jenkins_instance --auto-approve
```

Before proceeding,make sure that you have setup ansible server in EC2 instance. Once that is done, run the following commands

```bash
sudo ansible-playbook playbooks/jenkins.yml
```
Once the playbook execution is done, you shall see the initial password in the terminal,copy the password and login to Jenkins server. Next click on the install suggested plugins and wait for installation to complete. Create a username and password for jenkins authentication.

Finally you can access the Jenkins Dashboard in EC2 instance on port 8080

#### Install Docker in Jenkins Instance
Before we install docker in jenkins instance, we need to have jenkins instance up and running. Once the jenkins instance is up and running, run the following commands, for docker installation

```bash
sudo ansible-playbook playbooks/docker.yml
```

#### Install Terraform in Jenkins Instance
Before we install docker in jenkins instance, we need to have jenkins instance up and running. Once the jenkins instance is up and running, run the following commands, for terraform installation

```bash
sudo ansible-playbook playbooks/terraform.yml
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

#### Setup Application instance
SSH into ansible server and run the commands to provision the application instance

```bash
terraform -chdir=infrastructure init
```

```bash
terraform -chdir=infrastructure apply -target=module.application_instance --auto-approve
```

#### Installing Tekton CLI
Before setting up tekton cli, make sure that application instance is up and runnning. Once that is done, run the playbook using the following command

```bash
sudo ansible-playbook playbooks/tektoncli.yml
```

### Setup application as service 
We need to run the application in the EC2 instance continuously without us running the start or stop commands. So, how do we achieve this ?
The approach is simple we need to run the application as service inside EC2 instance. In order to do so we need run the application.yml playbook

```bash
sudo ansible-playbook playbooks/application.yml
```

On successfull execution of application playbook, we can access the application on ec2 public ip with port as 8080, and that is it. Our application is set up as service in EC2 instance

On this is done, go to the jenkins dashsboard and click on "manage jenkins" and then click on "manage plugins" and in search bar type "ssh agent" and install the plugin. This plugin shall use private ssh key which will connect to application ec2 instance and perform CD of application code.

### How to perform CI CD for application microservice ??
Now that the previous step we have created our flask app as a service. The question is how to patch any new changes made to application source code. In simple CI CD to flask application running as a service in EC2 instance. Well, the approach is very simple, we shall use Jenkins and Git to do so, the workflow is fairly simple, first new application code is merged to main branch, on the commiting to the main branch, Jenkins will perform a series of steps which include connecting to the EC2 instance and getting the application_cicd.sh bash file from the repo and executing it. The bash file consists of commands wchich will get the source from Github, and stops the service and installs requirements.txt file and restarts nginx and application service, and that is it we are able to achieve CI CD for application service running in the ec2 instance, since Jenkins runs this stage when there is application code change. 

One thing to note that the filename "app.py" should be same, else the application might not work, since the initial setup was done using application "app.py" as filename. If we want change that to something else, make the neccessary changes to app.service file

### MLFlow setup in EC2 instance
For setting up mlflow in EC2 instance, SSH into ansible server and then run following commands to provision mlflow instance

```bash
terraform -chdir=infrastructure init
```

```bash
terraform -chdir=infrastructure apply -target=module.mlflow_instance --auto-approve
```

Once the mlflow instance is provisioned, run the commands to setup mlflow in EC2 instance

```bash
sudo ansible-playbook playbooks/mlflow.yml
```

If these commands do not return any error that means mlflow service is setup in EC2 instance, and can be accessed via public ip on ports 8000 or 8080. Go to the browser, and paste PUBLIC_IP:8080 or PUBLIC_IP:8000.

If everything is done properly, we should then see the mlflow dashboard in our browser.Sometimes, you might be prompted to give your username and password for login, remember that username and password is the same which have configured for nginx. The public ip with port, mlflow username and mlflow password acts as a environment variables when using model training service. 

### MongoDB Setup
Since we are using MongoDB as the database. We are using MongoDB Altas and terraform to provision the db instance. Before we provision the instance we need to export some environment variables such mongodb public key and private key. These keys can be accessed from the mongodb altas website by going into organizaation access manager and click on API keys and then create an API key and store the public key and private key somewhere safe and export it environment variables

```bash
export MONGODB_ATLAS_PUBLIC_KEY="your_public_key"
```

```bash
export MONGODB_ATLAS_PRIVATE_KEY="your_private_key"
```
To provision the mongodb altas database

```bash
terraform apply -target=module.mongodb_database
```
After the provisioning of database is done,store the database connection string in jenkins. 

### EKS cluster setup
Since we are using microservices architecture, kubernetes plays an important role in microservices architecture by orchestrating and managing our containters/microservices in the cloud. In AWS cloud, there is managed serviced called Elastic Kubernetes Service which allows us to create kubernetes cluster on AWS cloud. In order to create a kubernetes, open code editor in infrastructure folder, and uncomment two modules one is eks_cluster and kube_master modules. The main purpose kube_master module, to control the kubernetes cluster from an EC2 instance and not from local machine. 

To create a kubernetes cluster, we have to execute the following commands,

```bash
terraform -chdir=infrastructure init
```

```bash
terraform -chdir=infrastructure apply -target=module.eks_cluster --auto-approve 
```
These commands will be initialize the backend required to run terraform and stores the state in s3 bucket. The terraform module includes the launch of 5 instances which are of type t2.medium, which approximately 20GB cluster node groups. 

Now you might be why that much big cluster ??. The answer is we need to setup tekton, ArgoCD and on top of that we need to run our microservices. So approximately we need might 20GB cluster. We can scale up and down by changing the cluster configuration in terraform files or by using autoscaler, or completely shift to serverless infrastructure. That option is left to end user itself. I have choosen provisioned cluster of 20GB which should be enough to run our applications.

### Tekton Setup
Since we are using tekton for pipeline orchestration, we need to setup tekton in eks cluster. tekton pipelines can be set up in eks cluster, by looking in the docuementation of Tekton. The setup can be done by executing the following commands

#### Installing Tekton pipelines
Before setting up tekton pipelines, make sure that tekton cli is runnning the application EC2 instance. Once that is done, run the following commands

```bash
sudo ansible-playbook playbooks/tekton.yml
```

On successful execution of the playbook, we can see that tekton dashboard url is avaiable with port, grab it and paste it in browser and tekton dashboard is avaiable.

### Prometheus and Grafana setup 

#### In AWS EKS cluster
Before setting up prometheus and grafana in EKS cluster,make sure that we have EKS cluster up and running. Once that is done, run the following commands 

```bash
sudo ansible-playbook playbooks/monitoring.yml
```

On successfull execution of the playbook, we will see that prometheus and grafana urls, are avaiable with ports, grab them and paste in the browser, prometheus dashboard will be seen without any login, but in case of grafana dashboard you shall prompted for password, the username is admin and password is prom-operator, we can change this setting, on successful login.

#### Prometheus setup in EC2 instances for EC2 metrics
Before we proceed to setting up prometheus in EC2 instance, we need to make sure that the ansible roles for prometheus and node exporter and installed within the ansible server, in order to do so run the following commands,

```bash
ansible-galaxy install --roles-path /home/ubuntu/playbooks/roles cloudalchemy.prometheus
```

```bash
ansible-galaxy install --roles-path /home/ubuntu/playbooks/roles cloudalchemy.node_exporter
```
Once these roles are installed in the playbooks folder, we have to execute following commands to setup prometheus in EC2 instance

```bash
sudo ansible-playbook playbooks/prometheus-ec2.yml
```
Make sure that update the IP addresses of the respective ec2 instances to be monitored.

### ArgoCD setup
Argo CD is a declarative, GitOps continuous delivery tool for Kubernetes.Application definitions, configurations, and environments should be declarative and version controlled. Application deployment and lifecycle management should be automated, auditable, and easy to understand.

To setup argocd in EKS cluster, make sure that EKS cluster is provisioned. Once that is done, run the following commands to setup ArgoCD using the playbook

```bash
sudo ansible-playbook playbooks/argocd.yml
```
On successfull execution of argocd playbook, we shall see the playbook will output argocd url, grab it and paste in the browser with https, and login with username and password as mentioned in /vars/variables.yml  

Now that ArgoCD is setup in EKS cluster, we have to tell ArgoCD will repository to monitor, and which resources to deploy. In order to do that go to dashboard, click on create application.

Give any application name, it does not matter. Project to be default. Sync policy to be automatic. In the repository url give the url of the CD repository and path needs to be "./components" since our manifest files are stored in components folder. 

In the cluster url, select default cluster we can use argocd to deploy to other cluster also. In the namespace section select the namespaces which was created to run tekton pipelines, and click on create and thats it ArgoCD now monitors the CD repo every 3 minutes to sync if they are any new changes in the git repo.

### Destroy everything and clean up the resources in cloud
Now that everthing is tested out and successfully executed, we destroy the resources created so that we do not incur more charges from AWS cloud. In order to do that run

Before we destroy everthing, we have to EC2 dashboard and in there go to load balancers and delete the load balancers, because since the load balancer is not managed by terraform it becomes difficult for terraform to destroy it. 

Also, empty the data present s3 buckets, if you want them make a backup of it and then empty them. Once these things are done execute

```bash
terraform -chdir=infrastructure destroy --auto-approve
```

Sometimes even after deleting the load balancers, terraform takes time to delete the VPC resources, if that is the case stop the destroy and manually delete the VPC from VPC dashboard, and then destroy the resources using terraform

That is all from my side regarding this project. Thank you and hope you learnt from it.
Feel free to contact me at sethusaim@gmail.com regarding any clarifactions or doubts regarding the project.
