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
    favorites = models.ManyToManyField(
        'City',
        through='FavoriteCity',
        related_name='subscribers',
        blank=True
    )

    def __str__(self):
        return f'{self.telegram_id} ({self.language})'

class City(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class FavoriteCity(models.Model):
    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'city'], name='unique_favourite_city')
        ]

    def __str__(self):
        return f"{self.user.telegram_id} → {self.city.name}"