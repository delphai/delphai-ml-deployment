#!/usr/bin/env bash

#1 Inject ml secrets into 
echo 'Injecting Secrets into the Virtual Mashine'
sleep 1
export TENANT_ID=$1
export APP_ID=$2
export SECRET_ID=$3
export SUBSCRIPTION_ID=$4

echo 'Installing Virtual Mashine dependencies(update and pip3)'
sleep 1
sudo apt update -y
sudo apt install python3-pip -y 

echo 'Cloning the Repo into the vm'
sleep 1
git clone https://ahmedmahmo:$7@github.com/delphai/$5.git
cd $5
PWD=$(pwd)
echo 'Installing Model dependencies'
python3 -m pip install -r requirments.txt
echo 'Start Training'
sleep 1
python3 src/train.py

echo 'Start Registration Model'
wget --quiet --show-progress --timestamping https://raw.githubusercontent.com/delphai/delphai-ml-deployment/master/register/register.sh
wget --quiet --show-progress --timestamping https://raw.githubusercontent.com/delphai/delphai-ml-deployment/master/register/register.py
chmod +x register.sh
./register.sh
python3 register.py model $5 $6


