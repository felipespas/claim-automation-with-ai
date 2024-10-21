# read the value from txt file
$resourceGroupName = Get-Content -Path C:\_Github\claim-automation-with-ai\deploy\resourceGroupName.txt

$subscription_id = "2edd29f5-689f-48c5-b93e-93723216ea91"

# call the python script to enable key access
python.exe deploy\enable-key-auth.py $resourceGroupName $subscription_id