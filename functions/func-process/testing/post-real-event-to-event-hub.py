import asyncio

from azure.eventhub import EventData
from azure.eventhub.aio import EventHubProducerClient

EVENT_HUB_CONNECTION_STR="Endpoint=sb://eventhub20241017.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=YD1CvHYHWjivXHv9NvUGZre+1mqwa4bJs+AEhPclrQM="
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

        message = "{\"directory\": \"638647313990000000\", \"callbackUrl\": \"" + callbackUrl + "\"}"

        event_data_batch.add(EventData(message))

        await producer.send_batch(event_data_batch)

callbackUrl = 'https://prod-37.eastus2.logic.azure.com/workflows/a91b5188902d44f6af43a641b39a40cb/runs/08584724722702020579129516340CU09/actions/HTTP_Webhook/run?api-version=2016-06-01&sp=%2Fruns%2F08584724722702020579129516340CU09%2Factions%2FHTTP_Webhook%2Frun%2C%2Fruns%2F08584724722702020579129516340CU09%2Factions%2FHTTP_Webhook%2Fread&sv=1.0&sig=F1m_oMBVPhNcnqiyM5WkpB-HpB1ErcFdnEU_lNPQTeQ'

asyncio.run(run(callbackUrl))

