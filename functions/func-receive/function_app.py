import azure.functions as func
import datetime
import json
import logging

app = func.FunctionApp()


@app.event_hub_message_trigger(arg_name="azeventhub", event_hub_name="incoming",
                               connection="EVENT_HUB_CONN_STR") 
def receive01(azeventhub: func.EventHubEvent):
    logging.info('Python EventHub trigger processed an event: %s',
                azeventhub.get_body().decode('utf-8'))
    
    message = azeventhub.get_body().decode('utf-8')

    try:
        message_json = json.loads(message)

        data = json.dumps(message_json, indent=4)

        print(data)

    except Exception as e:
        logging.info("Message is not formatted as JSON")

    