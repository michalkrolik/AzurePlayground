variable "resource_group_name" {
  type        = string
}

variable "azure_datalake_name" {
  type        = string
}

variable "key_vault_name" {
  type        = string
}

variable "adls_secret" {
  type        = string
}

provider "azurerm" {
  features {}
  skip_provider_registration = true
}

data "azurerm_client_config" "current" {}

resource "azurerm_resource_group" "main" {
  name      = var.resource_group_name
  location  = "Germany West Central"
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
  name               = "candf-instagram"
  storage_account_id = azurerm_storage_account.main.id
}

resource "azurerm_storage_data_lake_gen2_path" "bronze" {
  path               = "bronze"
  filesystem_name    = azurerm_storage_data_lake_gen2_filesystem.main.name
  storage_account_id = azurerm_storage_account.main.id
  resource           = "directory"
}

resource "azurerm_storage_data_lake_gen2_path" "silver" {
  path               = "silver"
  filesystem_name    = azurerm_storage_data_lake_gen2_filesystem.main.name
  storage_account_id = azurerm_storage_account.main.id
  resource           = "directory"
}

resource "azurerm_storage_data_lake_gen2_path" "gold" {
  path               = "gold"
  filesystem_name    = azurerm_storage_data_lake_gen2_filesystem.main.name
  storage_account_id = azurerm_storage_account.main.id
  resource           = "directory"
}

resource "azurerm_key_vault" "main" {
  name                = var.key_vault_name
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  tenant_id           = data.azurerm_client_config.current.tenant_id
  sku_name            = "standard"
}

resource "azurerm_key_vault_secret" "storage_account_key" {
  name         = var.adls_secret
  value        = azurerm_storage_account.main.primary_access_key
  key_vault_id = azurerm_key_vault.main.id
  depends_on = [
    azurerm_key_vault_access_policy.main
  ]
}

resource "azurerm_role_assignment" "main" {
  principal_id         = data.azurerm_client_config.current.object_id
  role_definition_name = "Key Vault Secrets User"
  scope                = azurerm_key_vault.main.id
}

resource "azurerm_key_vault_access_policy" "main" {
  key_vault_id = azurerm_key_vault.main.id
  tenant_id    = data.azurerm_client_config.current.tenant_id
  object_id    = data.azurerm_client_config.current.object_id

  secret_permissions = [
    "Get",
    "List",
    "Set",
  ]
}

#Data Factory
variable "datafactory_name" {
  type        = string
}

variable "source_resource_group_name" {
  type        = string
}

variable "source_cosmosdb_endpoint" {
  type        = string
}

variable "source_cosmosdb_primary_key" {
  type        = string
}

variable "cosmosdblinkedservice" {
  type        = string
}

variable "source_cosmosdb_database" {
  type        = string
}

variable "source_cosmosdb_collection" {
  type        = string
}

variable "adls_account_key" {
  type        = string
}

variable adlslinkedservice {
  type        = string
}

variable adls_url {
  type        = string
}

resource "azurerm_data_factory" "main" {
  name                = var.datafactory_name
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
}

resource "azurerm_data_factory_linked_service_cosmosdb" "main" {
  name             = var.cosmosdblinkedservice
  data_factory_id  = azurerm_data_factory.main.id
  account_endpoint = var.source_cosmosdb_endpoint
  account_key      = var.source_cosmosdb_primary_key
  database         = var.source_cosmosdb_database
}

resource "azurerm_data_factory_linked_service_data_lake_storage_gen2" "main" {
  name                = var.adlslinkedservice
  data_factory_id     = azurerm_data_factory.main.id
  url                 = var.adls_url
  storage_account_key = var.adls_account_key
}

variable databricks_name {
  type = string
}

variable databricks_cluster_name {
  type = string
}

variable databricks_workspace_token {
  type = string
}

variable databricks_instance {
  type = string
}

resource "azurerm_databricks_workspace" "main" {
  name                = var.databricks_name
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  sku                 = "premium"
}

provider "databricks" {
  host  = var.databricks_instance
  token = var.databricks_workspace_token
}

resource "databricks_cluster" "main" {
  cluster_name            = var.databricks_cluster_name
  spark_version           = "7.3.x-scala2.12"
  node_type_id            = "Standard_DS3_v2"
  autotermination_minutes = 20
  num_workers             = 0

  spark_conf = {
    "spark.databricks.cluster.profile" = "singleNode"
    "spark.master"                     = "local[*]"
    "fs.azure.account.key.${var.azure_datalake_name}.dfs.core.windows.net" = "{{secrets/mySecretScope/adls-access-key}}"
  }
  depends_on = [azurerm_databricks_workspace.main]
}

resource "databricks_secret_scope" "my_secret_scope" {
  name = "mySecretScope"
}

resource "databricks_secret" "adls_access_key" {
  key          = "adls-access-key"
  string_value = var.adls_account_key
  scope        = databricks_secret_scope.my_secret_scope.name
}
