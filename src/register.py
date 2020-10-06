import os
import json

from azureml.core import Workspace, Experiment, Run, Model
from azureml.core.authentication import ServicePrincipalAuthentication
from azureml.core.resource_configuration import ResourceConfiguration
from azureml.exceptions import AuthenticationException, ProjectSystemException, UserErrorException, ModelPathNotFoundException, WebserviceException
from adal.adal_error import AdalError
from msrest.exceptions import AuthenticationError
from json import JSONDecodeError

def register(model_path:str):
    # Load credentials 
    print("::debug::Loading azure credentials")
    azure_credentials = os.environ.get("INPUT_AZURE_CREDENTIALS", default="{}")
    try:
        azure_credentials = json.loads(azure_credentials)
    except JSONDecodeError:
        print("::error::Please paste output of `az ad sp create-for-rbac --name <your-sp-name> --role contributor --scopes /subscriptions/<your-subscriptionId>/resourceGroups/<your-rg> --sdk-auth` as value of secret variable: AZURE_CREDENTIALS")
        raise AMLConfigurationException("Incorrect or poorly formed output from azure credentials saved in AZURE_CREDENTIALS secret. See setup in https://github.com/Azure/aml-compute/blob/master/README.md")
    
    #destribute credentials over variables
    tenant_id       = azure_credentials['tenantId']
    app_id          = azure_credentials['clientId']
    app_secret      = azure_credentials['clientSecret']
    subscription_id = azure_credentials['subscriptionId']
    rm_endpoint     = azure_credentials['resourceManagerEndpointUrl']

    #Load model name and model version
    print("::debug::Loading input values")
    model_name = os.environ.get("INPUT_MODEL_NAME", default=None)
    mv = os.environ.get("INPUT_MODEL_VERSION", default=None) 

    #convert into int
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
    
    # Authenticate Azure
    try:
        sp = ServicePrincipalAuthentication(tenant_id=tenant_id,
        service_principal_id=app_id,
        service_principal_password=app_secret,
        cloud=cloud)
    except AuthenticationException as exception:
        print(f"::error::Could not retrieve user token. Please paste output of `az ad sp create-for-rbac --name <your-sp-name> --role contributor --scopes /subscriptions/<your-subscriptionId>/resourceGroups/<your-rg> --sdk-auth` as value of secret variable: AZURE_CREDENTIALS: {exception}")
        raise AuthenticationException
    
    #Load workspace and resource group
    print("::debug::Loading Workspace values")
    ws_path        = os.environ.get("INPUT_WORKSPACE")
    resource_group = os.environ.get("INPUT_RESOURCE_GROUP")
    
    #Load Azure workspace
    try:
        ws = Workspace.get(name=ws_path,auth=sp,subscription_id=subscription_id,resource_group=resource_group)
    except AuthenticationException as exception:
        print(f"::error::Could not retrieve user token. Please paste output of `az ad sp create-for-rbac --name <your-sp-name> --role contributor --scopes /subscriptions/<your-subscriptionId>/resourceGroups/<your-rg> --sdk-auth` as value of secret variable: AZURE_CREDENTIALS: {exception}")
        raise AuthenticationException
    
    try:
        model = Model.register(
                workspace=ws,
                model_path=model_path,
                model_name=parameters.get("model_name", default_model_name)[:32],
                tags="delphai"
            )
    except TypeError as exception:
        print(f"::error::Model could not be registered: {exception}")
        raise AMLConfigurationException("Model could not be registered")
    except WebserviceException as exception:
        print(f"::error::Model could not be registered: {exception}")
        raise AMLConfigurationException("Model could not be registered")  


