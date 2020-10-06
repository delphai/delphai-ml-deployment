
provider "azurerm" {
  features {}
  client_id       = var.client_id
  subscription_id = var.subscription_id
  tenant_id       = var.tenant_id
  client_secret   = var.client_secret
}

terraform {
  backend "azurerm" {
    resource_group_name  = "base-infrastructure-terraform"
    key                  = "base-infrastructure.tfstate"
    storage_account_name = "delphaicommon"
    container_name       = "delphai-common-ml-deployment-terraform-state"
  }
}

module "virtual_mashine" {
  source = "../modules/virtual_mashine"
  ssh    = var.ssh
}
