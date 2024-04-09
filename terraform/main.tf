terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "3.93.0"
    }
  }

  required_version = "1.7.3"
}

provider "azurerm" {
  features {}
}

data "azurerm_client_config" "current" {}

variable "suffix" {
  description = "The suffix for the resources"
  type        = string
}

variable "resourceGroupName" {
  description = "The name of the resource group"
  type        = string
}

variable "location" {
  description = "The location of the resource group"
  type        = string
}

resource "azurerm_resource_group" "rg" {
  name = var.resourceGroupName
  location = var.location
}

resource "azurerm_storage_account" "datalake_res" {
  name                              = "datalake${var.suffix}"
  resource_group_name               = azurerm_resource_group.rg.name
  location                          = azurerm_resource_group.rg.location
  account_tier                      = "Standard"
  account_replication_type          = "LRS"
  account_kind                      = "StorageV2"
  is_hns_enabled                    = "true"
  public_network_access_enabled     = "true"  
}

resource "azurerm_storage_data_lake_gen2_filesystem" "datalake_emails" {
  name               = "emails"
  storage_account_id = azurerm_storage_account.datalake_res.id
}

resource "azurerm_storage_data_lake_gen2_filesystem" "datalake_jsons" {
  name               = "jsons"
  storage_account_id = azurerm_storage_account.datalake_res.id
}

resource "azurerm_service_plan" "function_plan" {
  name                = "functionplan${var.suffix}"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  os_type             = "Linux"
  sku_name            = "Y1"
}

resource "azurerm_storage_account" "storage_fn" {
  name                     = "functionstg${var.suffix}"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_log_analytics_workspace" "log_analytics" {
  name                = "loganalytics${var.suffix}"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  sku                 = "PerGB2018"
  retention_in_days   = 30
}

resource "azurerm_application_insights" "app_insights" {
  name                = "appinsights${var.suffix}"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  workspace_id        = azurerm_log_analytics_workspace.log_analytics.id
  application_type    = "other"
}

resource "azurerm_linux_function_app" "function_app" {
  name                = "functionapp${var.suffix}"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location

  storage_account_name       = azurerm_storage_account.storage_fn.name
  storage_account_access_key = azurerm_storage_account.storage_fn.primary_access_key
  service_plan_id            = azurerm_service_plan.function_plan.id

  site_config {
    application_stack {
      python_version = "3.11"
    }
    application_insights_key = azurerm_application_insights.app_insights.instrumentation_key
  }

  identity {
    type = "SystemAssigned"
  }
}

resource "azurerm_cognitive_account" "azure_ai_services" {
  name                = "aiservices${var.suffix}"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  kind                = "CognitiveServices"
  sku_name = "S0" 
}

resource "azurerm_logic_app_workflow" "logic_app" {
  name                = "logicapp${var.suffix}"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  identity {
    type = "SystemAssigned"
  }
}

resource "azurerm_key_vault" "key_vault" {
  name                        = "keyvault${var.suffix}2"
  location                    = azurerm_resource_group.rg.location
  resource_group_name         = azurerm_resource_group.rg.name
  enabled_for_disk_encryption = true
  tenant_id                   = data.azurerm_client_config.current.tenant_id
  soft_delete_retention_days  = 7
  purge_protection_enabled    = false
  sku_name = "standard"
}

resource "azurerm_role_assignment" "logic_app_blob_contributor" {
  scope                = azurerm_storage_account.datalake_res.id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id         = azurerm_logic_app_workflow.logic_app.identity[0].principal_id
  depends_on = [ azurerm_logic_app_workflow.logic_app ]
}

resource "azurerm_role_assignment" "function_blob_contributor" {
  scope                = azurerm_storage_account.datalake_res.id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id         = azurerm_linux_function_app.function_app.identity[0].principal_id
  depends_on           = [ azurerm_storage_account.datalake_res, azurerm_linux_function_app.function_app ]
}

resource "azurerm_role_assignment" "logic_apps_secret_user" {
  scope                = azurerm_key_vault.key_vault.id
  role_definition_name = "Key Vault Secrets User"
  principal_id         = azurerm_logic_app_workflow.logic_app.identity[0].principal_id
  depends_on           = [ azurerm_logic_app_workflow.logic_app, azurerm_key_vault.key_vault ]
}

resource "azurerm_role_assignment" "felipe_secret_user" {
  scope                = azurerm_key_vault.key_vault.id
  role_definition_name = "Key Vault Secrets Officer"
  principal_id         = data.azurerm_client_config.current.object_id
  depends_on           = [ azurerm_key_vault.key_vault ]
}