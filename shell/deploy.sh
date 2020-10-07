#!/usr/bin/env bash

cd /app/infrastructure/main
terraform init
terraform apply -auto-approve  -var tenant=$1 -var app_id=$2 -var app_secret=$3 -var subscription_id=$4 -var repo_name=$5
echo 'Making Sure puplic Ip is avilable...(Try Again)'
sleep 2
terraform apply -auto-approve  -var tenant=$1 -var app_id=$2 -var app_secret=$3 -var subscription_id=$4 -var repo_name=$5
