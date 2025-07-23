from functools import wraps

from asgiref.sync import sync_to_async
from django.conf import settings

from bot.models import TelegramUser


def with_user_language(handler):
    @wraps(handler)
    async def wrapper(update, context):
        try:
            user = await sync_to_async(TelegramUser.objects.get)(
                    telegram_id=update.effective_user.id
            )
            lang = user.language
        except TelegramUser.DoesNotExist:
            lang = settings.LANGUAGE_CODE

        context.user_lang = lang
        return await handler(update, context)

    return wrapper