# Generated by Django 5.1.5 on 2025-01-21 21:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("journal", "0002_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="diaryentry",
            options={"verbose_name": "запись", "verbose_name_plural": "записи"},
        ),
    ]
