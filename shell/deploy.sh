#!/usr/bin/env bash
echo 'Set Up Dependencies'
apt-get install unzip
wget https://releases.hashicorp.com/terraform/0.13.4/terraform_0.13.4_linux_amd64.zip
unzip terraform_0.13.4_linux_amd64.zip
mv terraform /usr/local/bin/

echo 'Moving to infrastrucure'
cd infrastructure/main
terraform init
terraform apply -auto-approve