#!bin/bash

git init

git remote remove origin

git remote add origin https://github.com/sethusaim/Wafer-Fault-Kubernetes.git

git fetch origin

git checkout origin/main -- ansible_playbooks

cd ansible_playbooks

sudo ansible-playbook playbooks/main.yml