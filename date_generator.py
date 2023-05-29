import lesson_types
import time_types
from datetime import datetime
import pytz

def format_time(time: int, type: str) -> str:
    if time % 10 == 1:
        if type == time_types.DAYS:
            return "день"
        elif type == time_types.HOURS:
            return "час"
    elif 2 <= time % 10 <= 4 and not (10 <= time % 100 <= 19):
        if type == time_types.DAYS:
            return "дня"
        elif type == time_types.HOURS:
            return "часа"
    else:
        if type == time_types.DAYS:
            return "дней"
        elif type == time_types.HOURS:
            return "часов"

def generate_date(month: int, day: int, lesson: str) -> str:
    time_now = datetime.now(pytz.timezone('Asia/Yekaterinburg'))
    time_delta = datetime(2023, month, day, 10, 00, tzinfo=pytz.timezone('Asia/Yekaterinburg')) - time_now
    out_str = ""    
    if lesson == lesson_types.MATH: 
        out_str = "ЕГЭ по математике"
    elif lesson == lesson_types.RUS:
        out_str = "ЕГЭ по русскому"
    elif lesson == lesson_types.INF:
        out_str = "ЕГЭ по инфе"
    elif lesson == lesson_types.PHYS:
        out_str = "ЕГЭ по физике"
    elif lesson == lesson_types.BIO:
        out_str = "ЕГЭ по биологии"

    if time_delta.days < 0:
        out_str = "<del>" + out_str + " прошел</del>\n"
        return out_str
    out_str += " через <tg-spoiler>"

    if time_delta.days > 10:
        out_str += f"{time_delta.days} {format_time(time_delta.days, time_types.DAYS)}"
    else:
        hours = int(time_delta.days) * 24 + int(time_delta.seconds) // 3600
        out_str += f"{hours} {format_time(hours, time_types.HOURS)}"
    out_str += "</tg-spoiler>\n"
    return out_str

