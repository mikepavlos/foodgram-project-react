from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(
        max_length=settings.EMAIL_LENGTH,
        unique=True,
    )
    first_name = models.CharField(blank=False,)
    last_name = models.CharField(blank=False,)
    password = models.CharField(max_length=settings.PASSWORD_LENGTH)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
