import requests

TOKEN = ""
WEBHOOK_URL = ""
url = f"https://api.telegram.org/bot{TOKEN}/setWebhook"
response = requests.post(url, json={"url": WEBHOOK_URL})

print(response.json())
