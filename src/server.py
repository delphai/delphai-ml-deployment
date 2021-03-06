import os
import json
from deploy import deploy
from json import JSONDecodeError

def main():
    azure_credentials_ml     = os.environ.get("INPUT_AZURE_CREDENTIALS_ML", default={})
    azure_credentials_common = os.environ.get("INPUT_AZURE_CREDENTIALS_COMMON", default={})
    train_action             = os.environ.get('INPUT_TRAIN') 
    deploy_action            = os.environ.get('INPUT_DEPLOY') 
    repo                     = os.environ.get('REPOSITORY_NAME')
    model_version            = os.environ.get("INPUT_MODEL_VERSION", default=None) 

    try: 
        #azure_credentials_ml     = json.loads(azure_credentials_ml)
        azure_credentials_common = json.loads(azure_credentials_common)
    except JSONDecodeError:
        print("::error::Please paste output of `az ad sp create-for-rbac --name <your-sp-name> --role contributor --scopes /subscriptions/<your-subscriptionId>/resourceGroups/<your-rg> --sdk-auth` as value of secret variable: AZURE_CREDENTIALS") 

    tenant_id       = azure_credentials_common['tenantId']
    app_id          = azure_credentials_common['clientId']
    app_secret      = azure_credentials_common['clientSecret'] 
    subscription_id = azure_credentials_common['subscriptionId']

    os.environ['ARM_CLIENT_ID']       = app_id
    os.environ['ARM_CLIENT_SECRET']   = app_secret
    os.environ['ARM_SUBSCRIPTION_ID'] = subscription_id
    os.environ['ARM_TENANT_ID']       = tenant_id

    github_password = os.environ.get('INPUT_GITHUB_PASSWORD')

    print(f'::debug::Train Action is {train_action}')
    if train_action == 'yes':
        os.system(f'/app/shell/deploy.sh {tenant_id} {app_id} {app_secret} {subscription_id} {repo} {model_version} {github_password}')
        os.system('/app/shell/destroy.sh')

    print(f'::debug::Deploy Action is {deploy_action}')
    if deploy_action == 'yes':
        deploy()
    
if __name__ == "__main__":
    main()