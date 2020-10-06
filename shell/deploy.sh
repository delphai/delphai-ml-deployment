#!/usr/bin/env bash
echo 'Set Up Dependencies'
apt-get install unzip
wget https://releases.hashicorp.com/terraform/0.13.3/terraform_0.13.3_linux_amd64.zip
unzip terraform_0.13.3_linux_amd64.zip
mv terraform /usr/local/bin/

echo 'Moving to infrastrucure'
cd /app/infrastructure/main
terraform --version
sleep 2
echo 'Start Deploying'
terraform init
terraform apply -auto-approve
echo 'Wait and tey again'
sleep 5
terraform apply -auto-approve