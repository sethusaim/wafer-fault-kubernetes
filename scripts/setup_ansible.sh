#!bin/bash

sudo apt update

sudo apt-get update

echo "Installing Terraform"

sudo apt-get update && sudo apt-get install -y gnupg software-properties-common curl

curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -

sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"

sudo apt-get update && sudo apt-get install terraform

echo "Installed Terraform"

echo "Installing Ansible"

sudo apt update

sudo apt-get update

sudo apt-add-repository -y ppa:ansible/ansible

sudo apt-get update

sudo apt-get install -y ansible

sudo apt install -y python3-pip

pip3 install boto3

ansible --version

sudo apt install awscli -y

pip3 install --upgrade awscli

echo "Installed Ansible"

echo "Setting up git repo"

git init 

git remote add origin https://github.com/sethusaim/Wafer-Fault-Kubernetes.git

git fetch origin main

git checkout origin/main -- infrastructure

git checkout origin/main -- playbooks

git checkout origin/main -- vars

echo "Git repo setup is done"

echo "Installing Prometheus node exporter role"

ansible-galaxy install --roles-path /home/ubuntu/playbooks/roles cloudalchemy.prometheus

echo "Installed prometheus role"

echo "Installing node exporter role"

ansible-galaxy install --roles-path /home/ubuntu/playbooks/roles cloudalchemy.node_exporter

echo "Installed node exporter role"