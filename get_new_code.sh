#!bin/bash
git init

git remote remove origin

git remote add origin https://github.com/sethusaim/Wafer-Fault-Kubernetes.git

git fetch origin

git checkout origin/main -- application
