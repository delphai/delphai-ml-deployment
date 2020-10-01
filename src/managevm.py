import os
import json
from azure.common.credentials import ServicePrincipalCredentials

from context import AzureContext 
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.compute import ComputeManagementClient
from haikunator import Haikunator

haikunator = Haikunator()

VM_REFERENCE = {
    'linux': {
        'publisher': 'Canonical',
        'offer'    : 'UbuntuServer',
        'sku'      : '16.04.0-LTS',
        'version'  : 'latest'
    }  
}

def managevm():
    # Load credentials 
    print("::debug::Loading azure credentials")
    azure_credentials = os.environ.get("INPUT_AZURE_CREDENTIALS", default="{}")
    try:
        with open('creds.json') as j_file:
            data = json.load(j_file)

        azure_credentials = json.loads(azure_credentials) or data
    except JSONDecodeError:
        print("::error::Please paste output of `az ad sp create-for-rbac --name <your-sp-name> --role contributor --scopes /subscriptions/<your-subscriptionId>/resourceGroups/<your-rg> --sdk-auth` as value of secret variable: AZURE_CREDENTIALS")
        raise AMLConfigurationException("Incorrect or poorly formed output from azure credentials saved in AZURE_CREDENTIALS secret. See setup in https://github.com/Azure/aml-compute/blob/master/README.md")
    
    #destribute credentials over variables
    tenant_id       = azure_credentials['tenantId']
    app_id          = azure_credentials['clientId']
    app_secret      = azure_credentials['clientSecret']
    subscription_id = azure_credentials['subscriptionId']

    # Authenticate Azure
    try:
        sp = ServicePrincipalAuthentication(tenant_id=tenant_id,
        service_principal_id=app_id,
        service_principal_password=app_secret
        )
    except:
        print('no auth')
    
    client = ComputeManagementClient(sp, subscription_id)
    print('Loading ...')
    vms = client.virtual_machines._start_initial(resource_group_name='sens2vec', vm_name='indexer')
    




    
managevm()