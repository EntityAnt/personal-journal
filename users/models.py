from django.contrib.auth.models import AbstractUser
from django.db import models

from config.settings import NULLABLE


class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True, verbose_name="Почта", help_text="Укажите почту"
    )
    phone = models.CharField(
        max_length=35,
        **NULLABLE,
        verbose_name="Телефон",
        help_text="Укажите номер телефона"
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

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"
