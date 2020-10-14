import yaml
import os

with open("src/conda.yml","r") as f:
    y = yaml.load(f, Loader=yaml.FullLoader)
    for dep in y['dependencies'][1]['pip']:
        os.system(f'pip3 install {dep}')