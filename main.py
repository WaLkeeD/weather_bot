# import logging
# import asyncio
# from aiogram import Bot, Dispatcher, types, F
# from aiogram.filters import Command
# import config

# # Получаем токен из конфигурационного файла
# API_TOKEN = config.token

# # Включаем логирование
# logging.basicConfig(level=logging.INFO)

# # Инициализация бота и диспетчера
# bot = Bot(token=API_TOKEN)
# dp = Dispatcher()

# # handler for /start
# @dp.message(Command('start'))
# async def cmd_start(message: types.Message):
#     name = message.chat.first_name
#     await message.answer(f'Hello, {name}. Enter "hello", "bye" or "how are you?" messages to get the answers!')
    

# # handler for /info
# @dp.message(Command('info'))
# async def cmd_info(message: types.Message):
#     name = message.chat.first_name
#     await message.answer(f'{name}, Information block works well')

# @dp.message(F.text)
# async def msg_echo(message: types.Message):
#     msg_user = message.text
#     name = message.chat.first_name
#     if 'Hello' in msg_user:
#         await message.answer(f'Hello, hello {name}!')
#     elif 'Bye' in msg_user:
#         await message.answer(f'Bye, {name}')
#     elif 'How are you?' in msg_user:
#         await message.answer(f'im good, and you?')
#     else:
#         await message.answer(f'I did not understand your message, {name}')

# # Основная функция запуска бота
# async def main():
#     await dp.start_polling(bot)

# if __name__ == '__main__':
#     asyncio.run(main())

import logging
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Router

# Замените 'YOUR_TELEGRAM_BOT_TOKEN' и 'YOUR_OPENWEATHER_API_KEY' на ваши токены
API_TOKEN = '7260666024:AAGTxSp-dQmKhKgBCRTIlNECSR4j2IiLkGU'
WEATHER_API_KEY = '1501a3346d4f7d82630b193b24cc86a2'
WEATHER_API_URL = 'http://api.openweathermap.org/data/2.5/weather'

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
router = Router()
dp.include_router(router)

# Команда /start
@router.message(Command(commands=['start']))
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я бот прогноза погоды. Введите команду в формате: \n'погода [город]'")

# Обработчик текстовых сообщений
@router.message()
async def get_weather(message: types.Message):
    try:
        # Вывод для отладки
        logging.info(f"Получено сообщение: {message.text}")

        # Разбираем сообщение
        parts = message.text.split()
        logging.info(f"Разобранные части: {parts}")

        if len(parts) != 2 or parts[0].lower() != 'погода':
            raise ValueError("Неправильный формат команды. Используйте: 'погода [город]'")

        city = parts[1]
        logging.info(f"Запрашиваем погоду для города: {city}")

        # Запрашиваем погоду
        params = {
            'q': city,
            'appid': WEATHER_API_KEY,
            'units': 'metric',  # Получаем температуру в градусах Цельсия
            'lang': 'ru'  # Получаем описание на русском языке
        }
        response = requests.get(WEATHER_API_URL, params=params)
        logging.info(f"Ответ API: {response.text}")

        if response.status_code != 200:
            raise ValueError("Не удалось получить прогноз погоды. Попробуйте позже.")

        weather_data = response.json()

        # Получаем данные о погоде
        temp = weather_data['main']['temp']
        description = weather_data['weather'][0]['description']
        humidity = weather_data['main']['humidity']
        wind_speed = weather_data['wind']['speed']

        # Формируем сообщение
        weather_message = (
            f"Погода в {city}:\n"
            f"Температура: {temp}°C\n"
            f"Описание: {description}\n"
            f"Влажность: {humidity}%\n"
            f"Скорость ветра: {wind_speed} м/с"
        )

        # Отправляем результат
        await message.reply(weather_message)

    except Exception as e:
        logging.error(f"Ошибка: {e}")
        await message.reply(f"Ошибка: {e}")

# Запуск бота
if __name__ == '__main__':
    import asyncio

    async def main():
        await dp.start_polling(bot)

    asyncio.run(main())





