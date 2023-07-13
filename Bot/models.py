import telebot
from django.db import models


class BotConfig(models.Model):
    title = models.CharField(
        verbose_name="title", max_length=80, blank=True, default=""
    )
    link = models.URLField(verbose_name="link", max_length=80, blank=True, default="")
    token = models.CharField(verbose_name="token", max_length=100, primary_key=True)
    server_url = models.CharField(
        verbose_name="Webhook Url", max_length=200, blank=True, default=""
    )
    is_active = models.BooleanField(default=True)

    def set_hook(self):
        bot = telebot.TeleBot(self.token)
        webhook_url = self.server_url + "/get_hook/"
        bot.set_webhook(webhook_url, drop_pending_updates=True)

    def set_active_config(self):
        if self.is_active:
            other_active_configs = BotConfig.objects.filter(is_active=True)
            for config in other_active_configs:
                if config.pk != self.pk:
                    config.is_active = False
                    config.save()

    def save(self, *args, **kwargs):
        self.set_hook()
        self.set_active_config()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Bot settings"
        verbose_name_plural = "Bot settings"
