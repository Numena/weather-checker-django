from django.db import models
from django.conf import settings

# Create your models here.

class TelegramUser(models.Model):
    telegram_id = models.CharField(max_length=64, unique=True)
    language = models.CharField(
        max_length=2,
        choices=settings.LANGUAGES,
        default=settings.LANGUAGE_CODE
    )

    def __str__(self):
        return f'{self.telegram_id} ({self.language}'

class FavoriteCity(models.Model):
    telegram_id = models.BigIntegerField()
    city = models.CharField(max_length=100)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['telegram_id', 'city'], name='unique_favourite_city')
        ]

    def __str__(self):
        return f"{self.telegram_id} → {self.city}"