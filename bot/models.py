from django.db import models

# Create your models here.


class FavoriteCity(models.Model):
    telegram_id = models.BigIntegerField()
    city = models.CharField(max_length=100)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['telegram_id', 'city'], name='unique_favourite_city')
        ]

    def __str__(self):
        return f"{self.telegram_id} → {self.city}"