#!bin/bash

terraform -chdir=infrastructure init

terraform -chdir=infrastructure destroy --auto-approve