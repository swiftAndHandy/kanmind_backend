from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserProfileManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class UserProfile(AbstractUser):
    objects = UserProfileManager()
    fullname = models.CharField("Full Name", max_length=255)
    USERNAME_FIELD = 'email'
    username = None
    email = models.EmailField(unique=True)
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email