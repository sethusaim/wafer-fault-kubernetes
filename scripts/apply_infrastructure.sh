#!bin/bash

terraform -chdir=infrastructure init

terraform -chdir=infrastructure apply --auto-approve