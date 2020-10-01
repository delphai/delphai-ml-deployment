from azure.common.credentials import ServicePrincipalCredentials

class AzureContext(object):
    def __init__(self, subscription_id, client_id, client_secret, tenant):
        self.credentials = ServicePrincipalCredentials(
            client_id=client_id,
            secret=client_secret,
            tenant=tenant
        )
        self.subscription_id = subscription_id