#!/usr/bin/env bash

#1 Inject ml secrets into 
export AZURE_CREDENTIALS_ML = $1

git clone https://github.com/delphai/dummy-trainer.git
cd dummy-trainer
python3 -m pip install -r requirments.txt
python3 train.py

cd ..
mkdir register
cd register
wget https://raw.githubusercontent.com/delphai/delphai-ml-deployment/master/register/requirments.txt
wget https://raw.githubusercontent.com/delphai/delphai-ml-deployment/master/register/register.py
python3 -m pip install -r requirments.txt
python3 register.py 


