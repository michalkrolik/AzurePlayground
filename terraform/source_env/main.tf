variable "resource_group_name" {
  type        = string
}

variable "cosmosdb_account_name" {
  type        = string
}

variable "cosmosdb_database_name" {
  type        = string
}

variable "cosmosdb_container_name" {
  type        = string
}

variable "azure_datalake_name" {
  type        = string
}
provider "azurerm" {
  features {}
  skip_provider_registration = true
}

resource "azurerm_resource_group" "main" {
  name      = var.resource_group_name
  location  = "Germany West Central"
}

resource "azurerm_cosmosdb_account" "main" {
  name                       = var.cosmosdb_account_name
  location                   = azurerm_resource_group.main.location
  resource_group_name        = azurerm_resource_group.main.name
  offer_type                 = "Standard"
  kind                       = "GlobalDocumentDB"
  analytical_storage_enabled = true

  consistency_policy {
    consistency_level = "Session"
  }

  geo_location {
    location          = azurerm_resource_group.main.location
    failover_priority = 0
  }
}

resource "azurerm_cosmosdb_sql_database" "main" {
  name                = var.cosmosdb_database_name
  resource_group_name = azurerm_resource_group.main.name
  account_name        = azurerm_cosmosdb_account.main.name
}

resource "azurerm_cosmosdb_sql_container" "main" {
  name                   = var.cosmosdb_container_name
  resource_group_name    = azurerm_resource_group.main.name
  account_name           = azurerm_cosmosdb_account.main.name
  database_name          = azurerm_cosmosdb_sql_database.main.name
  partition_key_paths    = ["/id"]
  throughput             = 400
  analytical_storage_ttl = -1
}

resource "azurerm_storage_account" "main" {
  name                     = var.azure_datalake_name
  resource_group_name      = azurerm_resource_group.main.name
  location                 = azurerm_resource_group.main.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  account_kind             = "StorageV2"
  is_hns_enabled           = "true"
}

resource "azurerm_storage_data_lake_gen2_filesystem" "main" {
  name               = "instagram"
  storage_account_id = azurerm_storage_account.main.id
}

resource "azurerm_storage_data_lake_gen2_path" "main" {
  path               = "media"
  filesystem_name    = azurerm_storage_data_lake_gen2_filesystem.main.name
  storage_account_id = azurerm_storage_account.main.id
  resource           = "directory"
}
