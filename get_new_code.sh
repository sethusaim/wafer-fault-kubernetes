#!bin/bash

git remote remove origin

git remote add origin https://github.com/sethusaim/WebApp-Service.git

git fetch origin

git checkout origin/main -- application