import os
import json
from deploy import deploy
from json import JSONDecodeError

def main():
    train = os.environ.get('INPUT_TRAIN', default=False) or True
    deploy= os.environ.get('INPUT_DEPLOY',default=False) or True
    if train == True:
        os.system('/app/shell/deploy.sh')
        os.system('/app/shell/destroy.sh')
        
    # if deploy == True:
    #     deploy()
    
if __name__ == "__main__":
    main()