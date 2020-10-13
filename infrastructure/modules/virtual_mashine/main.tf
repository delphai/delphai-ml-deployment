# Create a resource group if it doesn't exist
resource "azurerm_resource_group" "main" {
    name     = "delphai-common-vm"
    location = "westeurope"

    tags = {
        environment = "common"
    }
}

# Create virtual network
resource "azurerm_virtual_network" "main" {
    name                = "MLVnet"
    address_space       = ["10.0.0.0/16"]
    location            = "westeurope"
    resource_group_name = azurerm_resource_group.main.name

    tags = {
        environment = "common"
    }
}

# Create subnet
resource "azurerm_subnet" "main" {
    name                 = "MLSubnet"
    resource_group_name  = azurerm_resource_group.main.name
    virtual_network_name = azurerm_virtual_network.main.name
    address_prefixes       = ["10.0.1.0/24"]
}

# Create public IPs
resource "azurerm_public_ip" "main" {
    name                         = "MLPublicIP"
    location                     = "westeurope"
    resource_group_name          = azurerm_resource_group.main.name
    allocation_method            = "Dynamic"

    tags = {
        environment = "common"
    }
}

# Create Network Security Group and rule
resource "azurerm_network_security_group" "main" {
    name                = "MLSecurityGroup"
    location            = "westeurope"
    resource_group_name = azurerm_resource_group.main.name
    
    security_rule {
        name                       = "SSH"
        priority                   = 1001
        direction                  = "Inbound"
        access                     = "Allow"
        protocol                   = "Tcp"
        source_port_range          = "*"
        destination_port_range     = "22"
        source_address_prefix      = "*"
        destination_address_prefix = "*"
    }

    tags = {
        environment = "common"
    }
}

# Create network interface
resource "azurerm_network_interface" "main" {
    name                      = "MLNIC"
    location                  = "westeurope"
    resource_group_name       = azurerm_resource_group.main.name

    ip_configuration {
        name                          = "MLNicConfiguration"
        subnet_id                     = azurerm_subnet.main.id
        private_ip_address_allocation = "Dynamic"
        public_ip_address_id          = azurerm_public_ip.main.id
    }

    tags = {
        environment = "common"
    }
}

# Connect the security group to the network interface
resource "azurerm_network_interface_security_group_association" "main" {
    network_interface_id      = azurerm_network_interface.main.id
    network_security_group_id = azurerm_network_security_group.main.id
}

# Generate random text for a unique storage account name
resource "random_id" "main" {
    keepers = {
        # Generate a new ID only when a new resource group is defined
        resource_group = azurerm_resource_group.main.name
    }
    
    byte_length = 8
}

# Create storage account for boot diagnostics
resource "azurerm_storage_account" "main" {
    name                        = "mlvm"
    resource_group_name         = azurerm_resource_group.main.name
    location                    = "westeurope"
    account_tier                = "Standard"
    account_replication_type    = "LRS"

    tags = {
        environment = "common"
    }
}



# Create virtual machine
resource "azurerm_linux_virtual_machine" "main" {
    name                  = "ml"
    location              = "westeurope"
    resource_group_name   = azurerm_resource_group.main.name
    network_interface_ids = [azurerm_network_interface.main.id]
    size                  = "Standard_DS1_v2"

    os_disk {
        name              = "MLOsDisk"
        caching           = "ReadWrite"
        storage_account_type = "Premium_LRS"
    }

    source_image_reference {
        publisher = "Canonical"
        offer     = "UbuntuServer"
        sku       = "18.04-LTS"
        version   = "latest"
    }

    computer_name  = "devops"
    admin_username = "devops"
    disable_password_authentication = true
        
    admin_ssh_key {
        username       = "devops"
        public_key     = file("/root/.ssh/id_rsa.pub")
    }

    boot_diagnostics {
        storage_account_uri = azurerm_storage_account.main.primary_blob_endpoint
    }

    tags = {
        environment = "common"
    }

}

resource "null_resource" "setup" {
    depends_on = [azurerm_linux_virtual_machine.main, azurerm_public_ip.main]
    connection {
    type        = "ssh"
    user        = "devops"
    private_key = file("/root/.ssh/id_rsa")
    host        = azurerm_public_ip.main.ip_address
  }
    provisioner "file" {
        source      = "/app/shell/script.sh"
        destination = "/tmp/script.sh"
   }

    provisioner "remote-exec" {
        inline = [
            "chmod +x /tmp/script.sh",
            "/tmp/script.sh ${var.tenant} ${var.app_id} ${var.app_secret} ${var.subscription_id} ${var.repo_name} ${var.model_version} ${var.github_password}",
    ]
  }
}

