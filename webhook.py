import requests
import json
import os

def post_webhook(message, timestamp, status, title, color=0):
    url = os.environ.get('WEBHOOK')
    data = {}
    data['embeds'] = []
    embed = {}
    embed['title'] = f'{title} Notice'
    embed['description'] = message
    embed['footer'] = {}
    embed['footer']['text'] = f'Alert state: {status}'
    embed['timestamp'] = timestamp
    embed['color'] = color
    data['embeds'].append(embed)
    print(data)
    result = requests.post(url, data=json.dumps(data), headers={"Content-Type": "application/json"})
    print(result)
    return result