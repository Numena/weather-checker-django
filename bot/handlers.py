import logging
from asgiref.sync import sync_to_async
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from django.conf import settings
from .models import TelegramUser
from .utils import with_user_language
from .i18n import tr

from bot.models import FavoriteCity
from bot.weather import get_weather
logger = logging.getLogger(__name__)

@with_user_language
async def start (update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(tr('start', context.user_lang))

# Change a language and save a user preference
@with_user_language
async def lang(update: Update, context: ContextTypes.DEFAULT_TYPE):
    code = (context.args[0].lower() if context.args else '').strip()
    choices = dict(settings.LANGUAGES)

    if code in choices:
        user, created = await sync_to_async(TelegramUser.objects.get_or_create)(
            telegram_id=update.effective_user.id
        )
        user.language = code
        await sync_to_async(user.save)()

        await update.message.reply_text(
            tr('lang_set', code, lang=choices[code])
        )
    else:
        await update.message.reply_text(
            tr('usage_lang', context.user_lang)
        )

@with_user_language
async def show_favorites(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    cities = await sync_to_async(list)(
        FavoriteCity.objects
        .filter(telegram_id=user_id)
        .values_list('city', flat=True)
    )

    if not cities:
        await update.message.reply_text(tr('no_cities', context.user_lang))
        return

    keyboard = [[KeyboardButton(city)] for city in cities]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(tr('choose'), context.user_lang, reply_markup=reply_markup)

@with_user_language
async def handle_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    city = update.message.text.strip()
    user_id = update.effective_user.id

    await sync_to_async(FavoriteCity.objects.get_or_create, thread_sensitive=True)(
        telegram_id=user_id, city=city
    )

    weather_data =  await get_weather(city)

    if 'error' in weather_data:
        await update.message.reply_text(
            tr('error', context.user_lang, weather_data['error'])
        )
        return

    await update.message.reply_text(tr('weather',context.user_lang,
    city=city.title(),
    temp = weather_data['temperature'],
    desc = weather_data['description']
))