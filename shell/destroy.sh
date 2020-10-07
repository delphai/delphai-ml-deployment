#!/usr/bin/env bash

cd /app/infrastructure/main
terraform init
terraform destroy -auto-approve