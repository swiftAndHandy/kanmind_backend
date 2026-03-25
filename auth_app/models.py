from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserProfileManager(BaseUserManager):
    """
    Custom manager required because username=None breaks Django's default UserManager.
    create_superuser delegates to create user after settings flags.
    """
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
    """
    Custom user model, replacing Django's default User.
    Uses email address as username for authentication.
    username is set None to remove it entirely.
    REQUIRED_FIELDS is emptied to avoid conflicts with USERNAME_FIELD.
    """
    objects = UserProfileManager()
    fullname = models.CharField("Full Name", max_length=255)
    USERNAME_FIELD = 'email'
    username = None
    email = models.EmailField(unique=True)
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email