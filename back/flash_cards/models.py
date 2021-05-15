from django.db import models


class FlashCard(models.Model):
    word = models.TextField()
    translation = models.TextField()
    creation_time = models.DateTimeField(auto_created=True)
    is_learned = models.BooleanField(default=False)

    class Meta:
        # TODO: Прописать мета-инвормацию о модели
        pass
