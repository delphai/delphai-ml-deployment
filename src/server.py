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

    #Load Model
    print("::debug::Loading model")
    try:
        model = Model(
            workspace=ws,
            name=model_name,
            version=model_version
        )
    except WebserviceException as exception:
        print(f"::error::Could not load model with provided details: {exception}")
        raise AMLConfigurationException(f"Could not load model with provided details: {exception}")

    # Loading deployment target
    print("::debug::Loading deployment target")
    try:
        deployment_target = ComputeTarget(
            workspace=ws,
            name=os.environ.get("INPUT_COMPUTE_TARGET")
        )
    except ComputeTargetException:
        deployment_target = None
    except TypeError:
        deployment_target = None

    # Loading entry and conda file
    print("::debug::Loading entry_file & Conda file")
    entry_file = os.environ.get("INPUT_ENTRY_FILE", default="entry.py")
    entry_file_path = os.path.join("src", entry_file)
    
    conda_file = os.environ.get("INPUT_CONDA_FILE", default="conda.yml")
    conda_ffile_path = os.path.join("src", conda_file)

    
    inference_config = InferenceConfig(
            entry_script= entry_file_path,
            runtime='python',
            conda_file=conda_ffile_path,
        )

    

    # Deploying model
    # print("::debug::Deploying model")
    # try:
    #     service = Model.deploy(workspace=ws,name=model_name,models=[model],inference_config=InferenceConfig,)

    




















if __name__ == "__main__":
    main()