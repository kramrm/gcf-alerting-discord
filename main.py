# gcf-alerting-discord.py

"Google Cloud Function to send Google Cloud Monitoring alerts to Discord via webhook"

import base64
import json
import os
from datetime import datetime, timezone
from typing import Any, Optional

import requests


def hello_pubsub(event: dict, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
        event (dict): Event payload.
        context (google.cloud.functions.Context): Metadata for the event.
    """
    pubsub_message = base64.b64decode(event["data"]).decode("utf-8")
    message = json.loads(pubsub_message)
    message = message["incident"]
    status = "Status"
    log_message = ""
    title = "Monitoring Alert"
    status = message["state"].title()
    timestamp = datetime.fromtimestamp(
        message["started_at"], tz=timezone.utc
    ).isoformat()
    log_message += f"Started: <t:{message["started_at"]}>"
    color = 16772608
    if message["ended_at"] is not None:
        timestamp = datetime.fromtimestamp(
            message["ended_at"], tz=timezone.utc
        ).isoformat()
        log_message += f"\nEnded: <t:{message["ended_at"]}>"
        color = 65297
    title = message["policy_name"]
    log_message += f'\n{message["summary"]}'
    log_message += f'\n[Monitor Event]({message["url"]})'
    post_webhook(
        message=log_message,
        timestamp=timestamp,
        status=status,
        title=title,
        color=color,
    )


def post_webhook(
    message: str, timestamp: str, status: str, title: str, color: Optional[int] = 0
):
    """Post webhook to Discord
    Set an environment variable for 'WEBHOOK' to point to the URI for your channel

    Attributes
        message (str): The message to put in the embed
        timestamp (str): ISO 8601 timestamp of the event
        status (str): Status of the event to put in the footer
        title (str): Stats of the build process for the embed title.  Defaults to 'Status'
        color (int): Color to use for embed highlight. Defaults to black
    Returns
        result (requests.result): Result of Requests post
    """
    url = os.environ.get("WEBHOOK")
    if not url:
        raise ValueError("No WEBHOOK env variable set")
    data: dict[str, Any] = {}
    data["embeds"] = []
    embed: dict[str, Any] = {}
    embed["title"] = f"{title} Notice"
    embed["description"] = message
    embed["footer"] = {"text": f"Alert state: {status}"}
    embed["timestamp"] = timestamp
    embed["color"] = color
    data["embeds"].append(embed)
    print(data)
    result = requests.post(
        url,
        data=json.dumps(data),
        headers={"Content-Type": "application/json"},
        timeout=10,
    )
    print(result)
    return result
