# Define parameters
param (
    [string]$tenant_id,
    [string]$subscription_id
)

# disable subscription selector:
az config set core.login_experience_v2=off
az config set core.enable_broker_on_windows=false

# Login using az cli
az login --tenant $tenant_id

# set subscription using az cli
az account set --subscription $subscription_id

# tenant microsoft non-production
Connect-AzAccount -Tenant $tenant_id -Subscription $subscription_id

# list all subscriptions and show only the subscription id and name
Get-AzSubscription -TenantId $tenant_id | Select-Object -Property Id, Name

# set subscription - MCAPS-Hybrid-REQ-37753-2022-Fassis
Set-AzContext -SubscriptionId $subscription_id
