import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import config

# Настраиваем логирование
logging.basicConfig(level=logging.INFO)

# Создаем бота и диспетчер
bot = Bot(token=config.BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Состояния для регистрации
class Registration(StatesGroup):
    waiting_for_invite = State()
    waiting_for_name = State()
    waiting_for_last_name = State()

# Команда /start
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я бот для онлайн-тренировок Primavera 🌿\n\nДля доступа введи код приглашения:")
    await Registration.waiting_for_invite.set()

# Проверка кода приглашения
@dp.message_handler(state=Registration.waiting_for_invite)
async def process_invite(message: types.Message, state: FSMContext):
    if message.text in config.INVITE_CODES:
        await message.answer("✅ Код принят! Отлично!\n\nТеперь введи своё имя:")
        await Registration.waiting_for_name.set()
    else:
        await message.answer("❌ Неверный код. Попробуй еще раз или обратись к тренеру.")

# Получение имени
@dp.message_handler(state=Registration.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(first_name=message.text)
    await message.answer(f"Приятно познакомиться, {message.text}! 👋\n\nТеперь введи свою фамилию:")
    await Registration.waiting_for_last_name.set()

# Получение фамилии и завершение
@dp.message_handler(state=Registration.waiting_for_last_name)
async def process_last_name(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    
    await message.answer(
        f"🎉 **Регистрация завершена!**\n\n"
        f"👤 **Твое имя:** {user_data['first_name']} {message.text}\n"
        f"🔐 **Статус:** Активный участник\n\n"
        f"Теперь ты будешь получать тренировки 3 раза в неделю:\n"
        f"• Понедельник в 9:00\n"
        f"• Среда в 9:00\n"
        f"• Пятница в 9:00\n\n"
        f"Первая тренировка придет в ближайший день тренировок!\n\n"
        f"Если есть вопросы - пиши @artembokij"
    )
    
    # Здесь потом будет запись в Google Sheets
    await state.finish()

# Простая команда для проверки
@dp.message_handler(commands=['help'])
async def cmd_help(message: types.Message):
    await message.answer(
        "📋 **Доступные команды:**\n"
        "/start - начать регистрацию\n"
        "/help - эта справка\n\n"
        "Бот автоматически присылает тренировки по расписанию."
    )

# Запуск бота
async def main():
    await dp.start_polling()

if __name__ == '__main__':
    asyncio.run(main())
