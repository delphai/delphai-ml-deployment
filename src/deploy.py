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

    tenant_id = azure_credentials['tenantId']
    print(tenant_id)
    sp = ServicePrincipalAuthentication(tenant_id='605f6d17-d10f-47bd-8145-8e5740e61669',service_principal_id='d62549cd-a593-4945-976e-ffa8f74f6d50',service_principal_password='eHRl7O-i_BDsc10pH.t3569mTO7MHKXpgm')
    print(sp)


if __name__ == "__main__":
    main()