import os
from deploy import deploy

def main():
    run   = os.environ.get('INPUT_RUN',   default=False)
    train = os.environ.get('INPUT_TRAIN', default=False)
    deploy= os.environ.get('INPUT_DEPLOY',default=False)
    
if __name__ == "__main__":
    deploy()