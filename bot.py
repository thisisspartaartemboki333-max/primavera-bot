import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


# ======================
# НАСТРОЙКИ
# ======================

BOT_TOKEN = os.getenv("BOT_TOKEN")  # токен будем хранить в Railway

logging.basicConfig(level=logging.INFO)


# ======================
# СОСТОЯНИЯ (шаги диалога)
# ======================

class Registration(StatesGroup):
    waiting_for_name = State()


# ======================
# ЗАПУСК БОТА
# ======================

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# ======================
# ХЭНДЛЕРЫ
# ======================

@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await message.answer(
        "Привет! 👋\n\n"
        "Для начала напиши, пожалуйста, *Фамилию и Имя* одним сообщением.",
        parse_mode="Markdown"
    )
    await state.set_state(Registration.waiting_for_name)


@dp.message(Registration.waiting_for_name)
async def get_name(message: Message, state: FSMContext):
    full_name = message.text.strip()

    await state.update_data(full_name=full_name)

    await message.answer(
        f"Спасибо! Я записал:\n\n"
        f"**{full_name}**\n\n"
        f"Скоро пришлю первую тренировку 💪",
        parse_mode="Markdown"
    )

    await state.clear()


# ======================
# MAIN
# ======================

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
