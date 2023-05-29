import os
import requests


chat_id = -1001561236768
telegram_api_token =  os.getenv("TELEGRAM_API_TOKEN")
response = requests.post(
    f"https://api.telegram.org/bot{telegram_api_token}/sendVideo",
    json={
        "chat_id": chat_id,
        "video": "https://sgoapp.ru/sdai_ege"
    }
).json()
