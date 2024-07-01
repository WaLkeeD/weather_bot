import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import config

# Получаем токен из конфигурационного файла
API_TOKEN = config.token

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Обработчик команды /start
@dp.message(Command(commands="start"))
async def send_welcome(message: types.Message):
    await message.answer("Приветственный блок работает отлично!")

@dp.message(Command(commands="info"))
async def send_info(message: types.Message):
    await message.answer("Information section works well!")

# Основная функция запуска бота
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
