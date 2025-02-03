from django.contrib.auth.models import AbstractUser
from django.db import models

from config.settings import NULLABLE


class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True, verbose_name="Почта", help_text="Укажите почту"
    )
    phone_number = models.CharField(
        max_length=20,
        verbose_name="Номер телефона",
        **NULLABLE,
        help_text="Введите номер телефона"
    )
    avatar = models.ImageField(
        upload_to=r"users/avatars",
        **NULLABLE,
        verbose_name="Аватар",
        help_text="Загрузите фото аватара"
    )
    tg_nick = models.CharField(
        max_length=50,
        **NULLABLE,
        verbose_name="ТГ-ник",
        help_text="Укажите телеграмм-ник"
    )
    token = models.CharField(max_length=100, verbose_name="Токен", **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"
        permissions = [
            ("can_block_user", "Возможность блокировки пользователя"),
        ]

