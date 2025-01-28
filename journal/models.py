from django.db import models

from users.models import User


class DiaryEntry(models.Model):
    title = models.CharField(
        max_length=100, verbose_name="Заголовок", help_text="Укажите заголовок"
    )
    content = models.TextField(
        verbose_name="Запись в дневнике", help_text="Оставьте запись в дневнике"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user",
        verbose_name="Владелец",
        help_text="Укажите автора записи",
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "запись"
        verbose_name_plural = "записи"
