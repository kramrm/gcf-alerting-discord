import base64
import json
from dateutil.parser import parse
from webhook import post_webhook
from datetime import datetime


def hello_pubsub(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    #post_webhook(message=f'{pubsub_message}', timestamp='now', status='status', title='title')
    message = json.loads(pubsub_message)
    message = message['incident']
    #post_webhook(message, timestamp, status, title='Monitoring'):
    null = None
    status = 'Status'
    log_message = ''
    title = 'Monitoring Alert'
    status = message['state'].title()
    timestamp = datetime.utcfromtimestamp(message["started_at"]).isoformat()
    log_message += f'Started: {timestamp} UTC'
    color = 16772608
    if message['ended_at'] is not None:
        timestamp = datetime.utcfromtimestamp(message["ended_at"]).isoformat()
        log_message += f'\nEnded: {timestamp} UTC'
        color = 65297
    title = message['policy_name']
    log_message += f'\n{message["summary"]}'
    log_message += f'\n[Monitor Event]({message["url"]})'
    post_webhook(message=log_message, timestamp=timestamp, status=status, title=title, color=color)
