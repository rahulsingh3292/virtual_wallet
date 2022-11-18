from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager


class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    is_premium_user = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    EMAIL_FIELD = None
    REQUIRED_FIELDS = ["first_name", "is_premium_user"]

    def __str__(self) -> str:
        return self.first_name + self.last_name

    @classmethod
    def is_user_exist(cls, username: str) -> bool:
        return cls.objects.filter(username=username).exists()
