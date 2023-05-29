import pytz
from datetime import datetime
import os
import openai
import requests
import json

openai.api_key = os.getenv("OPENAI_TOKEN")
telegram_api_token = os.getenv("TELEGRAM_API_TOKEN")
promt = "Сгенерируй гороскоп для"
chat_id = -1001963131928
horo_promt = ["Овнов", "Тельцов", "Близнецов", "Раков", "Львов", "Дев", "Весов", "Скорпионов", "Стрельцов", "Козерогов",
              "Водолев", "Рыб"]
horo = ["Овен", "Телец", "Близнецы", "Рак", "Лев", "Дева", "Весы", "Скорпион", "Стрелец", "Козерог", "Водолей", "Рыбы"]

time_now = datetime.now(tz=pytz.timezone('Asia/Yekaterinburg'))
output_str = f"Гороскоп на {time_now.strftime('%d.%m.%Y')}:\n"
for i in range(len(horo_promt)):
    response = openai.Completion.create(model="text-davinci-003",
                                        prompt=f"{promt} {horo_promt[i]} на {time_now.strftime('%d %B %Y')} год. И оценки состояние здоровья {horo_promt[i]} на этот день по шкале от 1 до 10. Формат ответа должен быть такой: [гороскоп].\n[Оценка состояния здоровья]",
                                        max_tokens=500
                                        )
    output_str += horo[i] + ":\n" + response["choices"][0]["text"] + "\n\n"
requests.post(
    f"https://api.telegram.org/bot{telegram_api_token}/sendMessage",
    json={
        "chat_id": chat_id,
        "text": output_str
    }
)
