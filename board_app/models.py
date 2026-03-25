from django.db import models

from auth_app.models import UserProfile


# Create your models here.
class Board(models.Model):
    title = models.CharField("Title", max_length=255)
    owner = models.ForeignKey(UserProfile, related_name='board_owner', on_delete=models.CASCADE)
    members = models.ManyToManyField(UserProfile, related_name='board_members')

    def __str__(self):
        return f"#{self.id}: {self.title}"