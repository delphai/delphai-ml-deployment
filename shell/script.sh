#!/usr/bin/env bash

git clone https://github.com/delphai/dummy-trainer.git
cd dummy-trainer
python3 -m pip install -r requirments.txt
python3 train.py

