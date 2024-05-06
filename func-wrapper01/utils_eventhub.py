import os
import json
import asyncio
import logging

from dotenv import load_dotenv
from azure.eventhub import EventData
from azure.eventhub.aio import EventHubProducerClient

load_dotenv()

event_hub_connection_string = os.environ["EVENT_HUB_CONNECTION_STR"]
event_hub_name = os.environ["EVENT_HUB_NAME"]

async def send_event(event_data: str):
    # Create a producer client to send messages to the event hub.
    # Specify a connection string to your event hubs namespace and
    # the event hub name.
    producer = EventHubProducerClient.from_connection_string(
        conn_str=event_hub_connection_string, eventhub_name=event_hub_name
    )
    async with producer:
        # Create a batch.
        event_data_batch = await producer.create_batch()

        # Add events to the batch.
        event_data_batch.add(EventData(event_data))

        # Send the batch of events to the event hub.
        await producer.send_batch(event_data_batch)

        



