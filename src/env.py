import os
import sys
import json
import importlib

from azureml.core import Workspace, Model, ContainerRegistry
from azureml.core.compute import ComputeTarget, AksCompute
from azureml.core.model import InferenceConfig, Environment
from azureml.core.webservice import AksWebservice, AciWebservice
from azureml.exceptions import ComputeTargetException, AuthenticationException, ProjectSystemException, WebserviceException
from azureml.core.authentication import ServicePrincipalAuthentication
from adal.adal_error import AdalError
from msrest.exceptions import AuthenticationError
from json import JSONDecodeError

sp = ServicePrincipalAuthentication(tenant_id="605f6d17-d10f-47bd-8145-8e5740e61669",
        service_principal_id="dbd334d3-f187-4857-99d7-60a0f0b7f151",
        service_principal_password="7o2OgU.cJ8noWDrqX7~FO8YNZzU~ecWIX4",
        cloud="AzureCloud")

ws = Workspace.get(name="delphai-development",auth=sp,subscription_id="f06d52b2-9e96-4549-b9da-a7e71dd3234a",resource_group="machine-learning")
envs = Environment.list(workspace=ws)

for env in envs:
    print(env)