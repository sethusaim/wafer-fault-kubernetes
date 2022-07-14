#!bin/bash

git init

git remote remove origin

git remote add origin https://github.com/sethusaim/Ansible-AWS-Demo.git

git fetch origin

git checkout origin/main -- playbooks

sudo ansible-playbook playbooks/main.yml