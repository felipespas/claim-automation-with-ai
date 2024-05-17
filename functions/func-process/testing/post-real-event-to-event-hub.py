import asyncio

from azure.eventhub import EventData
from azure.eventhub.aio import EventHubProducerClient

EVENT_HUB_CONNECTION_STR="Endpoint=sb://eventhub150524.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=KPxXfsaDb/+dKtxwCcFR+hThABfX/pMwk+AEhFWWhZM="
EVENT_HUB_NAME="incoming"

async def run(callbackUrl:str):
    # Create a producer client to send messages to the event hub.
    # Specify a connection string to your event hubs namespace and
    # the event hub name.
    producer = EventHubProducerClient.from_connection_string(
        conn_str=EVENT_HUB_CONNECTION_STR, eventhub_name=EVENT_HUB_NAME
    )
    async with producer:
        # Create a batch.
        event_data_batch = await producer.create_batch()

        message = "{\"directory\": \"638514836840000000\", \"callbackUrl\": \"" + callbackUrl + "\"}"

        event_data_batch.add(EventData(message))

        await producer.send_batch(event_data_batch)

callbackUrl = 'https://prod-25.eastus.logic.azure.com/workflows/a88d0f2d8ca5499b9f46beefe63c502c/runs/08584857198117669067911377693CU53/actions/HTTP_Webhook/run?api-version=2016-06-01&sp=%2Fruns%2F08584857198117669067911377693CU53%2Factions%2FHTTP_Webhook%2Frun%2C%2Fruns%2F08584857198117669067911377693CU53%2Factions%2FHTTP_Webhook%2Fread&sv=1.0&sig=eKp4aTlRbPACajqiovaA1VOv4O1L-NxYdvR2kH4s8ew'

asyncio.run(run(callbackUrl))

