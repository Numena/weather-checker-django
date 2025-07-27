import logging
import os

from django.core.management.base import BaseCommand
from dotenv import load_dotenv
from telegram import BotCommand
from telegram.ext import (ApplicationBuilder, CommandHandler, MessageHandler, filters, )

from bot.handlers import start, show_favorites, handle_city, lang

logger = logging.getLogger(__name__)

COMMANDS = [
    ('start', 'Start bot'),
    ('favorites', 'Show favorite cities'),
    ('lang', 'Change your language')
]

COMMAND_HANDLERS = {
    'start': start,
    'favorites': show_favorites,
    'lang': lang,
}

class Command(BaseCommand):
    help = 'Launches the Telegram bot'

    def handle(self, *args, **kwargs):
        load_dotenv()
        token = os.getenv('TELEGRAM_TOKEN')
        if not token:
            raise Exception('TELEGRAM_TOKEN is not set in .env')


        app = ApplicationBuilder().token(token).build()

        for cmd_name, handler_fn in COMMAND_HANDLERS.items():
            app.add_handler(CommandHandler(cmd_name, handler_fn))

        app.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_city)
        )

        async def set_commands(application):
            bot_commands = [BotCommand(name, desc) for name, desc in COMMANDS]
            await application.bot.set_my_commands(bot_commands)
            logger.info('Bot commands set: %s', bot_commands)

        app.post_init = set_commands
        app.run_polling(close_loop=False)

