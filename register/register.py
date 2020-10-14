import os
import json

from azureml.core import Workspace, Experiment, Run, Model
from azureml.core.authentication import ServicePrincipalAuthentication
from azureml.core.resource_configuration import ResourceConfiguration
from azureml.exceptions import AuthenticationException, ProjectSystemException, UserErrorException, ModelPathNotFoundException, WebserviceException
from adal.adal_error import AdalError
from msrest.exceptions import AuthenticationError
from json import JSONDecodeError

def register(model_path:str, model_name:str, model_version:str):
    tenant_id       = os.environ.get('TENANT_ID') 
    app_id          = os.environ.get('APP_ID') 
    app_secret      = os.environ.get('SECRET_ID') 
    subscription_id = os.environ.get('SUBSCRIPTION_ID') 

    #Load model name and model version
    print("::debug::Loading input values")
    model_name = model_name
    mv = model_version

    #convert into int
    print("::debug::Casting input values")
    try:
        model_version = int(mv)
    except TypeError as exception:
        print(f"::debug::Could not cast model version to int: {exception}")
        model_version = None   

    
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
    ws_path        = "delphai-common-ml"
    resource_group = "tf-ml-workspace"
    
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
                model_name=model_name,
            )
    except TypeError as exception:
        print(f"::error::Model could not be registered: {exception}")

if __name__ == "__main__":
    from sys import argv
    model_path    = argv[1]
    model_name    = argv[2]
    model_version = argv[3]
    register(model_path=model_path, model_name=model_name, model_version=model_version)



