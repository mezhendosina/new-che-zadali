import base64
import logging
import os
import lesson_types
from datetime import datetime

import pytz
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ContentType

from check_ege.check_ege import CheckEge
from propusk_leaders import extract_propusk
from date_generator import generate_date

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=os.getenv("TELEGRAM_API_TOKEN"), connections_limit=2)

# storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# class Form(StatesGroup):
#     file = State()
#     captcha = State()


# @dp.message_handler(commands=["when_ege"])
# async def send_when_ege(message: types.Message):
#     time_now = datetime.now(pytz.timezone('Asia/Yekaterinburg'))

#     math = generate_date(6, 1, lesson_types.MATH)
#     russ = generate_date(5, 29, lesson_types.RUS)
#     inf = generate_date(6, 20, lesson_types.INF)
#     phys = generate_date(6, 5, lesson_types.PHYS)
#     bio = generate_date(6, 13, lesson_types.BIO)
#     text = math + russ + inf + phys + bio

#     await message.answer(text, parse_mode="HTML")


# @dp.message_handler(commands=["propusk_leaders"])
# async def send_propusk_leaders(message: types.Message):
#     # if message.from_user.username == "mezhendosina" and message.chat.type != "private":
#     # 	table = await message.answer(
#     # 		extract_propusk.get_table(),
#     # 		parse_mode="Markdown",
#     # 		disable_notification=True,
#     # 		disable_web_page_preview=True
#     # 	)
#     # 	await bot.pin_chat_message(table.chat.id, table.message_id, True)
#     # 	with open("propusk_leaders/message_id", "w") as f:
#     # 		f.write(f"{table.message_id} {table.chat.id}")
#     # elif message.chat.type == "private":
#     await message.answer(
#         extract_propusk.get_table(),
#         parse_mode="Markdown",
#         disable_notification=True,
#         disable_web_page_preview=True
#     )


# elif message.chat.type != "private":
# 	await bot.delete_message(message.chat.id, message.message_id)


# @dp.message_handler(state='*', commands='cancel')
# async def send_cancel(message: types.Message, state: FSMContext):
#     await state.finish()
#     await message.answer("Ок")


# @dp.message_handler(commands=["register_propusk_leader"])
# async def send_register_propusk_leader(message: types.Message):
#     if message.chat.type == "private":
#         await Form.file.set()

#         await message.reply(
#             "Ок, чтобы попасть в топ пропускающих необходимо отправить боту файл с отчетом о своей успеваемости и посещаемости по этой инструкции: mezhendosina.notion.site/d2a6d327d12440d2b8602d0416d2bc4b\n"
#             "Для отмены отправь /cancel"
#         )
#     else:
#         await message.reply("Чтобы попасть в рейтинг отсутствующих, напиши в личку @che_zadaliBot")


# @dp.message_handler(state=Form.file, content_types=ContentType.ANY)
# async def process_file(message: types.Message, state: FSMContext):
#     if message.document is not None:
#         if message.document.file_name.split(".")[-1] == "xls":
#             file = await bot.download_file_by_id(message.document.file_id)
#             try:
#                 propusks = await extract_propusk.extract_propusk(file)
#                 extract_propusk.save_propusk(
#                     message.from_user.first_name,
#                     message.from_user.id,
#                     message.from_user.username,
#                     propusks
#                 )

#                 await state.finish()
#                 await message.answer("Количество пропусков сохранено")
#                 propusk_get_table = extract_propusk.get_table()
#                 await message.answer(
#                     propusk_get_table,
#                     parse_mode="Markdown",
#                     disable_notification=True,
#                     disable_web_page_preview=True
#                 )

#             except Exception as e:
#                 logging.critical(e)
#                 await message.reply("При обработке отчета произошла ошибка")
#         else:
#             await message.reply("Это не тот файл. Нужна .xsl таблица")
#     else:
#         await message.reply("Это не файл")


# ege = CheckEge()


# @dp.message_handler(commands=["mezhendosina_ege"])
# async def mezhendosina_ege(message: types.Message):
#     if message.from_user.username == "mezhendosina":
#         if ege.captcha is None:
#             await Form.captcha.set()
#             ca = await ege.get_captcha()
#             await bot.send_photo(
#                 message.chat.id,
#                 base64.b64decode(ca["Image"])
#             )
#         else:
#             results = await ege.get_exams()
#             await bot.send_message(message.chat.id, results, parse_mode="html")
#     else:
#         await message.reply("Ты не @mezhendosina")


# @dp.message_handler(state=Form.captcha, content_types=ContentType.TEXT)
# async def process_captcha(message: types.Message, state: FSMContext):
#     await ege.login("04407189f06dc6f7bbd5285fcf3207c7", "386121", message.text)
#     results = await ege.get_exams()
#     await bot.send_message(message.chat.id, results, parse_mode="html")
#     await state.finish()


@dp.message_handler(commands=["mezhendosina_uni"])
async def mezhendosina_uni(message: types.Message):
    with open("check_uni/unis") as f:
        await bot.send_message(message.chat.id, parse_mode="Markdown", text=f.read())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
