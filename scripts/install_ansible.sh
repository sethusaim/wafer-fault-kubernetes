#!bin/bash

sudo apt update

sudo apt-get update

sudo apt-add-repository -y ppa:ansible/ansible

sudo apt-get update

sudo apt-get install -y ansible

sudo apt install -y python3-pip

pip3 install boto3

ansible --version