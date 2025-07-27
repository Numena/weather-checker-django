import logging
from asgiref.sync import sync_to_async
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from django.conf import settings
from .models import TelegramUser, City
from .types import WeatherInfo
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
        await sync_to_async(user.save, thread_sensitive=True)()

        context.user_lang = code

        await update.message.reply_text(
            tr('lang_set', context.user_lang, lang=choices[code])
        )
    else:
        await update.message.reply_text(
            tr('usage_lang', context.user_lang)
        )

@with_user_language
async def show_favorites(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    user, _ = await sync_to_async(TelegramUser.objects.get_or_create)(
        telegram_id=str(user_id)
    )

    cities = await sync_to_async(lambda:list(user.favorites.values_list('name', flat=True)))()

    if not cities:
        await update.message.reply_text(tr('no_cities', context.user_lang))
        return

    keyboard = [[KeyboardButton(city)] for city in cities]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(tr('choose'), context.user_lang, reply_markup=reply_markup)

@with_user_language
async def handle_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    city_name = update.message.text.strip()
    user_id = str(update.effective_user.id)

    user, _ = await sync_to_async(TelegramUser.objects.get_or_create, thread_sensitive=True)(telegram_id=user_id)

    if context.user_lang != user.language: context.user_lang = user.language

    city_obj, _ = await sync_to_async(City.objects.get_or_create, thread_sensitive=True)(name=city_name)

    await sync_to_async(user.favorites.add, thread_sensitive=True)(city_obj)

    result = await get_weather(city_name, context.user_lang)

    if result is None:
        await update.message.reply_text(
            tr('error', context.user_lang, error='WeatherFetchFailed')
        )
        return

    assert isinstance(result, WeatherInfo)
    await update.message.reply_text(
        tr(
            'weather',
            context.user_lang,
            city=result.city.title(),
            temp = result.temperature,
            desc = result.description
        )
    )
