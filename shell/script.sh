#!/usr/bin/env bash

sudo apt update -y 
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install python3.8 -y
sudo apt install python3-pip -y


git clone https://github.com/delphai/dummy-trainer.git
cd dummy-trainer
python3 -m pip install -r requirments.txt
python3 train.py

