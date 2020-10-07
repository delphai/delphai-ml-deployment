
provider "azurerm" {
  features {}
}

terraform {
  backend "azurerm" {
    resource_group_name  = "base-infrastructure-terraform"
    key                  = "base-infrastructure.tfstate"
    storage_account_name = "delphaicommon"
    container_name       = "delphai-common-ml-terraform-state"
  }
}

module "virtual_mashine" {
  source          = "../modules/virtual_mashine"
  tenant          = var.tenant
  app_id          = var.app_id
  app_secret      = var.app_secret
  subscription_id = var.subscription_id
}
