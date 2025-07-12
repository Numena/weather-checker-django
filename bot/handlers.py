import logging
from asgiref.sync import sync_to_async
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

from bot.models import FavoriteCity
from bot.weather import get_weather
logger = logging.getLogger(__name__)

async def start (update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        """Hello! Type the name of a city and send it.
For example: New York
To use commands Tap the menu at the bottom

Привет! Введи название города и отправь
Пример: Нью-Йорк
Чтобы использовать команды нажмите кнопку меню""")

async def show_favorites(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    cities = await sync_to_async(list)(
        FavoriteCity.objects
        .filter(telegram_id=user_id)
        .values_list('city', flat=True)
    )

    if not cities:
        await update.message.reply_text('You dont have chosen cities, yet')
        return

    keyboard = [[KeyboardButton(city)] for city in cities]
    await update.message.reply_text(
        'Choose the city:',
    )
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text('Choose the city:', reply_markup=reply_markup)

async def handle_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    city = update.message.text.strip()
    user_id = update.effective_user.id

    await sync_to_async(FavoriteCity.objects.get_or_create, thread_sensitive=True)(
        telegram_id=user_id, city=city
    )

    weather_data =  await get_weather(city)

    if 'error' in weather_data:
        await update.message.reply_text(f"Error: {weather_data['error']}")
        return

    temp = weather_data['temperature']
    desc = weather_data['description']
    await update.message.reply_text(f'{city.title()}: {temp}°C, {desc}')