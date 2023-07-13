# Generated by Django 4.2.3 on 2023-07-06 23:24

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="BotConfig",
            fields=[
                (
                    "title",
                    models.CharField(
                        blank=True, default="", max_length=80, verbose_name="title"
                    ),
                ),
                (
                    "link",
                    models.URLField(
                        blank=True, default="", max_length=80, verbose_name="link"
                    ),
                ),
                (
                    "token",
                    models.CharField(
                        max_length=100,
                        primary_key=True,
                        serialize=False,
                        verbose_name="token",
                    ),
                ),
                (
                    "server_url",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=200,
                        verbose_name="Webhook Url",
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={
                "verbose_name": "Bot settings",
                "verbose_name_plural": "Bot settings",
            },
        ),
    ]