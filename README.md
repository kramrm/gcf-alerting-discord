# gcf-alerting-discord

This is a Google Cloud Function to read Google Alerting status messages from Pub/Sub and relay those to a Discord webhook

## Setup

To set which server receives these messages, when creating the Function, set an environment variable called `WEBHOOK` to be the URL for your Discord channel.
