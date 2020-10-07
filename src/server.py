import os
import json
from deploy import deploy
from json import JSONDecodeError

def main():
    train = os.environ.get('INPUT_TRAIN', default=False) or True
    deploy= os.environ.get('INPUT_DEPLOY',default=False) or True

    azure_credentials_ml     = os.environ.get("INPUT_AZURE_CREDENTIALS_ML", default=get_local_ml_creds())
    azure_credentials_common = os.environ.get("INPUT_AZURE_CREDENTIALS_COMMON", default=get_local_common_creds())
    print(azure_credentials_common)
    tenant_id       = azure_credentials_common['tenantId']
    app_id          = azure_credentials_common['clientId']
    app_secret      = azure_credentials_common['clientSecret']
    subscription_id = azure_credentials_common['subscriptionId']
    rm_endpoint     = azure_credentials_common['resourceManagerEndpointUrl']

    os.environ['ARM_CLIENT_ID']       = app_id
    os.environ['ARM_CLIENT_SECRET']   = app_secret
    os.environ['ARM_SUBSCRIPTION_ID'] = subscription_id
    os.environ['ARM_TENANT_ID']       = tenant_id

    
    if train == True:
        os.system('/app/shell/deploy.sh')
        #os.system('/app/shell/destroy.sh')
        
    # if deploy == True:
    #     deploy(azure_credentials_ml)
    
def get_local_common_creds():
    with open('creds.json') as json_file:
        data = json.load(json_file)
    return data

def get_local_ml_creds():
    with open('register/creds.json') as json_file:
        data = json.load(json_file)
    return data

if __name__ == "__main__":
    main()