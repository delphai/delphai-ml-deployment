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
git clone https://github.com/delphai/$5.git
cd dummy-trainer
echo 'Installing Model dependencies'
python3 -m pip install -r requirments.txt
echo 'Start Training'
sleep 1
python3 train.py

echo 'Start Registration Model'
cd ..
mkdir register
cd register
wget https://raw.githubusercontent.com/delphai/delphai-ml-deployment/master/register/requirments.txt
wget https://raw.githubusercontent.com/delphai/delphai-ml-deployment/master/register/register.py
python3 -m pip install -r requirments.txt
python3 register.py /home/devops/$5/model $5 $6


