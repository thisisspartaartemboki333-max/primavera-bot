import os
import json
from datetime import datetime, timedelta

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import CommandStart
import asyncio

import gspread
from google.oauth2.service_account import Credentials


BOT_TOKEN = os.getenv("BOT_TOKEN")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
GOOGLE_CREDS_JSON = os.getenv("GOOGLE_CREDS_JSON")

# --- Google Sheets ---
creds_dict = json.loads(GOOGLE_CREDS_JSON)
scopes = ["https://www.googleapis.com/auth/spreadsheets"]
credentials = Credentials.from_service_account_info(creds_dict, scopes=scopes)
gc = gspread.authorize(credentials)
sheet = gc.open_by_key(SPREADSHEET_ID).sheet1


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "Привет! 👋\n\n"
        "Для начала напиши, пожалуйста, *Фамилию и Имя* одним сообщением.",
        parse_mode="Markdown"
    )


@dp.message(F.text)
async def save_user(message: Message):
    name_confirm = message.text.strip()

    if len(name_confirm.split()) < 2:
        await message.answer("Пожалуйста, введи *Фамилию и Имя*.")
        return

    telegram_id = message.from_user.id
    today = datetime.now().strftime("%d.%m.%Y")
    end_date = (datetime.now() + timedelta(days=30)).strftime("%d.%m.%Y")

    # Проверка — есть ли пользователь уже
    ids = sheet.col_values(1)
    if str(telegram_id) in ids:
        await message.answer("Ты уже есть в системе ✅")
        return

    sheet.append_row([
        telegram_id,
        name_confirm,
        today,
        end_date,
        0,  # Сделано тренировок
        0,  # Пропущено тренировок
        today
    ])

    await message.answer(
        "✅ Ты добавлен в систему!\n\n"
        f"📅 Подписка до: {end_date}"
    )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
