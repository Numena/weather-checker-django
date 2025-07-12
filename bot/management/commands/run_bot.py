import logging
import os

from django.core.management.base import BaseCommand
from dotenv import load_dotenv
from telegram import BotCommand
from telegram.ext import (ApplicationBuilder, CommandHandler, MessageHandler, filters, )

from bot.handlers import start, show_favorites, handle_city

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Launches the Telegram bot'

    def handle(self, *args, **kwargs):
        load_dotenv()
        token = os.getenv('TELEGRAM_TOKEN')
        if not token:
            raise Exception('TELEGRAM_TOKEN is not set in .env')


        app = ApplicationBuilder().token(token).build()

        app.add_handler(CommandHandler('start', start))
        app.add_handler(CommandHandler('favorites', show_favorites))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_city))

        async def set_commands(application):
            await application.bot.set_my_commands([
                BotCommand('start', 'Start bot'),
                BotCommand('favorites', 'Show favorite cities'),
            ])
            logger.info('Bot is working')

        app.post_init = set_commands
        app.run_polling(close_loop=False)

