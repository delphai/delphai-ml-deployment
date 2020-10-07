import os
import json
from deploy import deploy
from json import JSONDecodeError

def main():
    azure_credentials_ml     = os.environ.get("INPUT_AZURE_CREDENTIALS_ML", default={})
    azure_credentials_common = os.environ.get("INPUT_AZURE_CREDENTIALS_COMMON", default={})
    train                    = os.environ.get('INPUT_TRAIN', default='no') 
    deploy                   = os.environ.get('INPUT_DEPLOY',default='no') 
    repo                     = os.environ.get('REPOSITORY_NAME')

    try: 
        azure_credentials_ml     = json.loads(azure_credentials_ml)
        azure_credentials_common = json.loads(azure_credentials_common)
    except JSONDecodeError:
        print("::error::Please paste output of `az ad sp create-for-rbac --name <your-sp-name> --role contributor --scopes /subscriptions/<your-subscriptionId>/resourceGroups/<your-rg> --sdk-auth` as value of secret variable: AZURE_CREDENTIALS") 

    tenant_id_ml       = azure_credentials_ml['tenantId']
    app_id_ml          = azure_credentials_ml['clientId']
    app_secret_ml      = azure_credentials_ml['clientSecret']
    subscription_id_ml = azure_credentials_ml['subscriptionId']

    os.environ['ARM_CLIENT_ID']       = azure_credentials_common['clientId']
    os.environ['ARM_CLIENT_SECRET']   = azure_credentials_common['clientSecret']
    os.environ['ARM_SUBSCRIPTION_ID'] = azure_credentials_common['subscriptionId']
    os.environ['ARM_TENANT_ID']       = azure_credentials_common['tenantId']

    if train == 'yes':
        os.system(f'/app/shell/deploy.sh {tenant_id_ml} {app_id_ml} {app_secret_ml} {subscription_id_ml} {repo}')
        os.system('/app/shell/destroy.sh')
        
    if deploy == 'yes':
        deploy(azure_credentials_ml)
    
if __name__ == "__main__":
    main()