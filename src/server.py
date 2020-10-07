import os
import json
from deploy import deploy
from json import JSONDecodeError

def main():
    train = os.environ.get('INPUT_TRAIN', default=False) 
    deploy= os.environ.get('INPUT_DEPLOY',default=False) 
    
    azure_credentials_ml     = os.environ.get("INPUT_AZURE_CREDENTIALS_ML", default={})
    azure_credentials_ml     = json.loads(azure_credentials_ml)
    azure_credentials_common = os.environ.get("INPUT_AZURE_CREDENTIALS_COMMON", default={})
    azure_credentials_common = json.loads(azure_credentials_common)

    print(azure_credentials_common)
    tenant_id_common       = azure_credentials_common['tenantId']
    app_id_common          = azure_credentials_common['clientId']
    app_secret_common      = azure_credentials_common['clientSecret']
    subscription_id_common = azure_credentials_common['subscriptionId']

    tenant_id_ml       = azure_credentials_ml['tenantId']
    app_id_ml          = azure_credentials_ml['clientId']
    app_secret_ml      = azure_credentials_ml['clientSecret']
    subscription_id_ml = azure_credentials_ml['subscriptionId']

    os.environ['ARM_CLIENT_ID']       = app_id_common
    os.environ['ARM_CLIENT_SECRET']   = app_secret_common
    os.environ['ARM_SUBSCRIPTION_ID'] = subscription_id_common
    os.environ['ARM_TENANT_ID']       = tenant_id_common

    repo = os.environ.get('REPOSITORY_NAME')
    
    if train == True:
        os.system(f'/app/shell/deploy.sh {tenant_id_ml} {app_id_ml} {app_secret_ml} {subscription_id_ml} {repo}')
        os.system('/app/shell/destroy.sh')
        
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