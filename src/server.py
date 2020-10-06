import os
import json
from deploy import deploy
from json import JSONDecodeError
from managevm import run_cmd_in_vm


def main():
    print("::debug::Loading azure credentials")
    azure_credentials = os.environ.get("INPUT_AZURE_CREDENTIALS_COMMON", default="{}")
    try:
        with open('creds.json') as j_file:
            data = json.load(j_file)

        azure_credentials = json.loads(azure_credentials) or data
    except JSONDecodeError:
        print("::error::Please paste output of `az ad sp create-for-rbac --name <your-sp-name> --role contributor --scopes /subscriptions/<your-subscriptionId>/resourceGroups/<your-rg> --sdk-auth` as value of secret variable: AZURE_CREDENTIALS")
        raise AMLConfigurationException("Incorrect or poorly formed output from azure credentials saved in AZURE_CREDENTIALS secret. See setup in https://github.com/Azure/aml-compute/blob/master/README.md")
    
    #destribute credentials over variables
    os.environ['ARM_TENANT_ID']       = azure_credentials['tenantId']
    os.environ['ARM_CLIENT_ID']       = azure_credentials['clientId']
    os.environ['ARM_CLIENT_SECRET']   = azure_credentials['clientSecret']
    os.environ['ARM_SUBSCRIPTION_ID'] = azure_credentials['subscriptionId']

    train = os.environ.get('INPUT_TRAIN', default=False) or True
    deploy= os.environ.get('INPUT_DEPLOY',default=False) or True
    if train == True:
        os.system('/app/powershell/deploy.sh')
        os.system('/app/powershell/ip.sh')
        os.system('/app/powershell/destroy.sh')
        
    # if deploy == True:
    #     deploy()
    
if __name__ == "__main__":
    main()