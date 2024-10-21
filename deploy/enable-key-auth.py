import argparse
from azure.identity import DefaultAzureCredential
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.storage.models import StorageAccountUpdateParameters

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Enable key access for Azure Storage account.")
parser.add_argument("resource_group_name", help="The name of the resource group.")
parser.add_argument("subscription_id", help="The subscription ID.")
args = parser.parse_args()

# Define your subscription ID, resource group name, and storage account name
resource_group_name = args.resource_group_name
subscription_id = args.subscription_id

# List my storage account names:
credential = DefaultAzureCredential()
storage_client = StorageManagementClient(credential, subscription_id)
storage_accounts = storage_client.storage_accounts.list_by_resource_group(resource_group_name)

print("Storage accounts in resource group '{}':".format(resource_group_name))
for account in storage_accounts:
    print(account.name)

    storage_account_name = account.name
    
    # Create a StorageManagementClient
    storage_client = StorageManagementClient(credential, subscription_id)

    # Update the storage account properties to disable key access
    update_params = StorageAccountUpdateParameters(
        allow_shared_key_access=True  # Set this to False to disable key access
    )

    # Update the storage account
    storage_account = storage_client.storage_accounts.update(
        resource_group_name,
        storage_account_name,
        update_params
    )

    print(f"Updated storage account '{storage_account_name}' to enable key access.")