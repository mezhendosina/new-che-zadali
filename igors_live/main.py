import os

import requests

telegram_api_token = os.getenv("TELEGRAM_API_TOKEN")
chat_id = -1001963131928

with open("/home/mezhendosina/che-zadali/igors_live/count_repeat", "r") as f:
    curr_value = int(f.read())

response = requests.post(
    f"https://api.telegram.org/bot{telegram_api_token}/sendDice",
    json={
        "chat_id": chat_id,
        "emoji": "🎲"
    }
).json()
if response["result"]["dice"]["value"] == 5:
    curr_value += 1
    requests.post(f"https://api.telegram.org/bot{telegram_api_token}/sendMessage",
                  json={
                      "chat_id": chat_id,
                      "text": str(curr_value)
                  })
else:
    curr_value = 0
    requests.post(f"https://api.telegram.org/bot{telegram_api_token}/sendMessage",
                  json={
                      "chat_id": chat_id,
                      "text": "Живем живем"
                  })
if curr_value >= 3:
    requests.post(f"https://api.telegram.org/bot{telegram_api_token}/sendAnimation",
                  json={
                      "chat_id": chat_id,
                      "animation": "CgACAgQAAxkDAAINmGRf1aYLUBSLs-VzTU-q45C7EontAALvAgACRtIMU01szJtHri3MLwQ"
                  })

with open("/home/mezhendosina/che-zadali/igors_live/count_repeat", "w") as f:
    f.write(str(curr_value))
