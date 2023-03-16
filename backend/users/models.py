from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import username_validator


class User(AbstractUser):
    username = models.CharField(
        'Пользователь',
        max_length=settings.USERNAME_LENGTH,
        unique=True,
        validators=[username_validator]
    )
    first_name = models.CharField(
        'имя',
        max_length=settings.USERNAME_LENGTH,
        blank=False,
    )
    last_name = models.CharField(
        'фамилия',
        max_length=settings.USERNAME_LENGTH,
        blank=False,
    )
    password = models.CharField(
        'пароль',
        max_length=settings.USERNAME_LENGTH,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Subscribe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber',
        verbose_name='Пользователь'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribing',
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscribe'
            )
        ]

    def __str__(self):
        return f'{self.user}-{self.author}'
