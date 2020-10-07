
provider "azurerm" {
  version = "=2.5.0"
  features {}
}

# terraform {
#   backend "azurerm" {
#     resource_group_name  = "base-infrastructure-terraform"
#     key                  = "base-infrastructure.tfstate"
#     storage_account_name = "delphaicommon"
#     container_name       = "delphai-common-ml-deployment-terraform-state"
#   }
# }

module "virtual_mashine" {
  source      = "../modules/virtual_mashine"
  ml_creds    = var.ml_creds
}
