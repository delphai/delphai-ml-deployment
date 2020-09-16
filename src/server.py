import os
import sys
import json
import importlib

from azureml.core import Workspace, Model, ContainerRegistry
from azureml.core.compute import ComputeTarget, AksCompute
from azureml.core.model import InferenceConfig
from azureml.core.webservice import AksWebservice, AciWebservice
from azureml.exceptions import ComputeTargetException, AuthenticationException, ProjectSystemException, WebserviceException
from azureml.core.authentication import ServicePrincipalAuthentication
from adal.adal_error import AdalError
from msrest.exceptions import AuthenticationError
from json import JSONDecodeError

def main():
    print("::debug::Loading azure credentials")
    azure_credentials = os.environ.get("INPUT_AZURE_CREDENTIALS", default="{}")
    try:
        azure_credentials = json.loads(azure_credentials)
    except JSONDecodeError:
        print("::error::Please paste output of `az ad sp create-for-rbac --name <your-sp-name> --role contributor --scopes /subscriptions/<your-subscriptionId>/resourceGroups/<your-rg> --sdk-auth` as value of secret variable: AZURE_CREDENTIALS")
        raise AMLConfigurationException("Incorrect or poorly formed output from azure credentials saved in AZURE_CREDENTIALS secret. See setup in https://github.com/Azure/aml-compute/blob/master/README.md")

    tenant_id       = azure_credentials['tenantId']
    app_id          = azure_credentials['clientId']
    app_secret      = azure_credentials['clientSecret']
    subscription_id = azure_credentials['subscriptionId']
    rm_endpoint     = azure_credentials['resourceManagerEndpointUrl']

    print("::debug::Loading input values")
    model_name = os.environ.get("INPUT_MODEL_NAME", default=None)
    mv = os.environ.get("INPUT_MODEL_VERSION", default=None) 

    print("::debug::Casting input values")
    try:
        model_version = int(mv)
    except TypeError as exception:
        print(f"::debug::Could not cast model version to int: {exception}")
        model_version = None   

    # Define target cloud
    if rm_endpoint.startswith("https://management.usgovcloudapi.net"):
        cloud = "AzureUSGovernment"
    elif rm_endpoint.startswith("https://management.chinacloudapi.cn"):
        cloud = "AzureChinaCloud"
    else:
        cloud = "AzureCloud"
    

    try:
        sp = ServicePrincipalAuthentication(tenant_id=tenant_id,
        service_principal_id=app_id,
        service_principal_password=app_secret,
        cloud=cloud)
    except AuthenticationException as exception:
        print(f"::error::Could not retrieve user token. Please paste output of `az ad sp create-for-rbac --name <your-sp-name> --role contributor --scopes /subscriptions/<your-subscriptionId>/resourceGroups/<your-rg> --sdk-auth` as value of secret variable: AZURE_CREDENTIALS: {exception}")
        raise AuthenticationException
    
    print("::debug::Loading Workspace values")
    ws_path = os.environ.get("INPUT_WORKSPACE")
    
    ws =Workspace.from_config(path=ws_path,auth=sp)
    print(ws)




















if __name__ == "__main__":
    main()