import os
import json
from paramiko import SSHClient, AutoAddPolicy, RSAKey, AutoAddPolicy
from azure.common.credentials import ServicePrincipalCredentials
from azure.identity import DefaultAzureCredential
from context import AzureContext 
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.compute import ComputeManagementClient

def authenticate():
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
    tenant_id       = azure_credentials['tenantId']
    app_id          = azure_credentials['clientId']
    app_secret      = azure_credentials['clientSecret']
    subscription_id = azure_credentials['subscriptionId']

    credential = ServicePrincipalCredentials(client_id=app_id, secret=app_secret, tenant=tenant_id)
    return credential,subscription_id

CREDENTIALS, SUBSCRIPTION_ID = authenticate()
compute_client = ComputeManagementClient(CREDENTIALS,SUBSCRIPTION_ID)


    
    
def start_vm(compute_client, resource_group:str , vm_name:str):
    vm = compute_client.virtual_machines.begin_start(resource_group, vm_name).result()
    print(f':debug: Starting {vm_name} virtul mashine...')
    vm.wait()
    

def stop_vm(compute_client, resource_group:str , vm_name:str):
    vm = compute_client.virtual_machines.begin_power_off(resource_group, vm_name)
    print(f':debug: Stoping {vm_name} virtual mashine...')
    vm.wait()
    
def run_cmd_in_vm(host:str,cmd:str):
    ssh = SSHClient()
    load_ssh = ssh.load_host_keys('public.pem')
    ssh.set_missing_host_key_policy(AutoAddPolicy())
    vm_connection = ssh.connect(hostname=host,username='devops')
    print('::debug:: Training Model')
    ssh.exec_command(cmd)

