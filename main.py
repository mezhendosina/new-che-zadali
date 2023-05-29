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
from propusk_leaders import extract_propusk
from date_generator import generate_date
# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=os.getenv("TELEGRAM_API_TOKEN"))
# bot = Bot(token="1200960980:AAEnQYLDuBZTwf0rxJNcjxm9qJhGLeqGEA8")

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class Form(StatesGroup):
	file = State()


@dp.message_handler(commands=["when_ege"])
async def send_when_ege(message: types.Message):
	math = generate_date(6, 1, lesson_types.MATH)
	russ = generate_date(5, 29, lesson_types.RUS)
	inf = generate_date(6, 20, lesson_types.INF)
	phys = generate_date(6, 5, lesson_types.PHYS)
	bio = generate_date(6, 13, lesson_types.BIO)
	text = russ + math + phys + bio + inf 
	       
	await message.answer(text, parse_mode="HTML")


@dp.message_handler(commands=["propusk_leaders"])
async def send_propusk_leaders(message: types.Message):
	# if message.from_user.username == "mezhendosina" and message.chat.type != "private":
	# 	table = await message.answer(
	# 		extract_propusk.get_table(),
	# 		parse_mode="Markdown",
	# 		disable_notification=True,
	# 		disable_web_page_preview=True
	# 	)
	# 	await bot.pin_chat_message(table.chat.id, table.message_id, True)
	# 	with open("propusk_leaders/message_id", "w") as f:
	# 		f.write(f"{table.message_id} {table.chat.id}")
	# elif message.chat.type == "private":
	await message.answer(
		extract_propusk.get_table(),
		parse_mode="Markdown",
		disable_notification=True,
		disable_web_page_preview=True
	)


# elif message.chat.type != "private":
# 	await bot.delete_message(message.chat.id, message.message_id)


@dp.message_handler(state='*', commands='cancel')
async def send_cancel(message: types.Message, state: FSMContext):
	await state.finish()
	await message.answer("Ок")


@dp.message_handler(commands=["register_propusk_leader"])
async def send_register_propusk_leader(message: types.Message):
	if message.chat.type == "private":
		await Form.file.set()

		await message.reply(
			"Ок, чтобы попасть в топ пропускающих необходимо отправить боту файл с отчетом о своей успеваемости и посещаемости по этой инструкции: mezhendosina.notion.site/d2a6d327d12440d2b8602d0416d2bc4b\n"
			"Для отмены отправь /cancel"
		)
	else:
		await message.reply("Чтобы попасть в рейтинг отсутствующих, напиши в личку @che_zadaliBot")


@dp.message_handler(state=Form.file, content_types=ContentType.ANY)
async def process_file(message: types.Message, state: FSMContext):
	if message.document is not None:
		if message.document.file_name.split(".")[-1] == "xls":
			file = await bot.download_file_by_id(message.document.file_id)
			try:
				propusks = await extract_propusk.extract_propusk(file)
				extract_propusk.save_propusk(
					message.from_user.first_name,
					message.from_user.id,
					message.from_user.username,
					propusks
				)

				await state.finish()
				await message.answer("Количество пропусков сохранено")
				propusk_get_table = extract_propusk.get_table()
				await message.answer(
					propusk_get_table,
					parse_mode="Markdown",
					disable_notification=True,
					disable_web_page_preview=True
				)

			except Exception as e:
				logging.critical(e)
				await message.reply("При обработке отчета произошла ошибка")
		else:
			await message.reply("Это не тот файл. Нужна .xsl таблица")
	else:
		await message.reply("Это не файл")


if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)
