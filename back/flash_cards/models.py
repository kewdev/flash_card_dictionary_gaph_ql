from django.contrib.auth.models import User
from django.db import models


class CardsGroup(models.Model):
    name = models.CharField(max_length=255)
    crated_at = models.DateTimeField(auto_created=True)
    is_verbose = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        db_table = 'card_groups'
        verbose_name = 'Card group'
        verbose_name_plural = 'Card groups'
        unique_together = (("name", "user"),)

    def __str__(self):
        return f'{self.name}_{self.pk}'


class FlashCard(models.Model):
    word = models.CharField(max_length=255)
    translation = models.CharField(max_length=255)
    cards_group = models.ForeignKey(CardsGroup, related_name='flash_card', on_delete=models.PROTECT, null=True, blank=True)
    crated_at = models.DateTimeField(auto_now_add=True, blank=True)
    last_revised_at = models.DateTimeField(null=True, blank=True)
    is_learned = models.BooleanField(default=False)

    class Meta:
        db_table = 'flash_cards'
        verbose_name = 'Flash card'
        verbose_name_plural = 'Flash cards'
        unique_together = (("cards_group", "word"),)

    def __str__(self):
        return f'{self.word}_{self.pk}'

