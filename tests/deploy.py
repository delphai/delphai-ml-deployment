import os
import sys
import json
import time
import requests
from azureml.core import Workspace, Model, ContainerRegistry
from azureml.core.compute import ComputeTarget, AksCompute
from azureml.core.model import InferenceConfig, Environment
from azureml.core.webservice import AksWebservice, AciWebservice
from azureml.exceptions import ComputeTargetException, AuthenticationException, ProjectSystemException, WebserviceException
from azureml.core.authentication import ServicePrincipalAuthentication
from adal.adal_error import AdalError
from msrest.exceptions import AuthenticationError
from json import JSONDecodeError

def deploy():
     # Load credentials 
    print("::debug::Loading azure credentials")
    with open('creds.json') as json_file:
        azure_credentials = json.load(json_file)
    
    #destribute credentials over variables
    tenant_id       = azure_credentials['tenantId']
    app_id          = azure_credentials['clientId']
    app_secret      = azure_credentials['clientSecret']
    subscription_id = azure_credentials['subscriptionId']
    rm_endpoint     = azure_credentials['resourceManagerEndpointUrl']

    #Load model name and model version
    print("::debug::Loading input values")
    model_name = 'newsletter-info'
    mv = '1'
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
    ws_path        = 'delphai-common-ml'
    resource_group = 'tf-ml-workspace'
    
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
            name='delphai-common'
        )
    except ComputeTargetException:
        deployment_target = None
    except TypeError:
        deployment_target = None

    # Loading entry and conda file
    source = 'tests/model'

    print("::debug::Loading entry_file & Conda file")
    entry_file = 'entry.py'
    entry_file_path = os.path.join(source, entry_file)
    
    conda_file = 'conda.yml'
    conda_ffile_path = os.path.join(source, conda_file)
    print(conda_ffile_path)

    try:
        env = Environment.from_conda_specification(name=model_name, file_path=conda_ffile_path)
    except:
        print(f'::debug:: failed to create environment from {conda_ffile_path}')

    try:
        inference_configration = InferenceConfig(entry_script= entry_file_path,environment=env)
    except:
        print(f'::debug:: Failed to create InferenceConfig')
    
        #print('::debug:: Make sure conda.yml and entry.py are in the [src] directory')
    
    print('::debug:: get namespace and replicas')
    replicas = os.environ.get('INPUT_REPLICAS') or '3'
    try:
        replicas = int(replicas)
    except TypeError as exception:
        print(f"::debug::Could not cast model version to int: {exception}")
        replicas = 3   

    deployment_name = os.environ.get('INPUT_DEPLOYMENT_NAME',default=model_name.replace("_","-"))
    create_namespace(app_id=app_id, app_secret=app_secret, tenant=tenant_id,namespace=deployment_name)
    deployment_configration= AksWebservice.deploy_configuration(autoscale_enabled=False, num_replicas=replicas,namespace=deployment_name)

    # Deploying model
    print("::debug::Deploying model")
    override = os.environ.get('INPUT_OVERRIDE') or 'yes'
    if override == 'yes':
        override = True
    elif override == 'no':
        override = False
    try:
        service = Model.deploy(
                workspace=ws,
                name=deployment_name,
                models=[model],
                inference_config=inference_configration,
                deployment_config=deployment_configration,
                deployment_target=deployment_target,
                overwrite=override
            )
        service.wait_for_deployment(show_output=True)
    except WebserviceException as exception:
        print(f"::error::Model deployment failed with exception: {exception}")
        service_logs = service.get_logs()

    # Give Time to Ku8 to create PODS 
    time.sleep(60)

    if service.state != "Healthy":
        try:
            service_logs = service.get_logs()
        except:
            print(f"::error::Model deployment Might be failied, Please check in lens for your deployments")


def create_namespace(app_id:str, app_secret:str, tenant:str, namespace:str):
    url = 'https://api.delphai.red/namespacer-master/namespace'
    body = {
    "app_id" : app_id,
    "app_secret":app_secret,
    "tenant_id": tenant,
    "name": namespace
            }
    requests.post(url=url, json=body)

deploy()