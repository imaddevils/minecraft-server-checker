import requests
import time

# Put the API URL and the Discord Webhook
api_url = 'MCSTATUS_API' # Ex: https://api.mcstatus.io/v2/status/java/hypixel.net
webhook_url = 'YOUR_WEBHOOK' # Self explainatory

def check_server_status():
    # Getting the server status from the API
    response = requests.get(api_url)
    data = response.json()

    # Get relevant information
    server_host = data.get('host', 'Unknown')
    online_status = data.get('online', False)
    player_count = data.get('players', {}).get('online', 0)
    player_list = [player['name_clean'] for player in data.get('players', {}).get('list', [])]
    motd = data.get('motd', {}).get('clean', '')

    # Make the embed message
    if online_status:
        color = 0x00FF00
        description = f"**Status**: Online\n**Players**: {player_count}\n**Playerlist**: {', '.join(player_list)}\n**MOTD**: {motd}"
    else:
        color = 0xFF0000
        description = f"**Status**: Offline"

    embed = {
        "title": f"{server_host} Server Status",
        "description": description,
        "color": color
    }

    # Send the embed message to the Discord webhook
    payload = {
        "embeds": [embed]
    }
    response = requests.post(webhook_url, json=payload)

    if response.status_code == 204:
        print("Webhook sent!")
    else:
        print(f"Failed to send webhook: {response.status_code}, {response.text}")

while True:
    check_server_status()
    time.sleep(120) # Wait every 2 minutes (120 seconds) before checking again
