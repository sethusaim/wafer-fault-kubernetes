#!bin/bash

rm -r application

git init

git remote remove origin

git remote add origin https://github.com/sethusaim/Wafer-Fault-Kubernetes.git

git fetch origin

git checkout origin/main -- application

sudo service stop app

cd application

pip3 install -r requirements.txt

sudo service nginx restart

sudo service app restart