from django.db import models
from django.contrib.auth.models import User, AbstractUser


class UserProfile(AbstractUser):
    full_name = models.CharField("Full Name", max_length=255)
    USERNAME_FIELD = 'email'
    username = None
    email = models.EmailField(unique=True)
    REQUIRED_FIELDS = []