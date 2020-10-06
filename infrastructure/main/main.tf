
provider "azurerm" {
  features {}
  client_id = "de07a5be-a3ec-4753-bda3-00891d3aaded"
  subscription_id = "4c22a33b-2b28-4630-a8f3-d48ac261e2ed"
  tenant_id = "605f6d17-d10f-47bd-8145-8e5740e61669"
  client_secret = "33lWasHCIm4-L3PMqGadY6T35TyROe_z.t"
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
  source = "../modules/virtual_mashine"
  ssh    = var.ssh
}
