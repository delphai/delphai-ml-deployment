#!/usr/bin/env bash

echo 'Destroying...'
cd /app/infrastructure/main
terraform init
terraform destroy -auto-approve