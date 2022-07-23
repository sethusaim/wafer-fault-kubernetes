#!bin/bash

currentDate=`date`

declare job_log_file="/home/ubuntu/cron_job_log.txt"

echo "Entered cron job execution script at $currentDate" >> "${job_log_file}"

kubectl delete --all pods

echo "Deleted all pods at $currentDate" >> "${job_log_file}"

kubectl delete --all pipelineruns

echo "Deleted all pipeline runs at $currentDate" >> "${job_log_file}"

echo "Exited cron job execution script at $currentDate" >> "${job_log_file}