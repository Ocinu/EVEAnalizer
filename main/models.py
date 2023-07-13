import base64
import uuid

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _


class Settings(models.Model):
    class ResponseChoices(models.TextChoices):
        CODE = "code", _("code")
        TOKEN = "token", _("token")

    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=250, blank=True)
    client_id = models.CharField(max_length=250, blank=True)
    secret_key = models.CharField(max_length=250, blank=True)
    base64_key = models.CharField(max_length=250, blank=True)
    base_url = models.URLField(max_length=250, blank=True)
    data_url = models.URLField(max_length=250, blank=True)
    redirect_url = models.URLField(max_length=250, blank=True)
    response_type = models.CharField(
        max_length=250, choices=ResponseChoices.choices, default=ResponseChoices.CODE
    )

    def save(self, *args, **kwargs):
        value = f"{self.client_id}:{self.secret_key}".encode("ascii")
        base64_bytes = base64.b64encode(value)
        encode_value = base64_bytes.decode("ascii")
        self.base64_key = encode_value
        self.set_active_setting()
        super().save(*args, **kwargs)

    def set_active_setting(self):
        if self.is_active:
            other_active_settings = Settings.objects.filter(is_active=True)
            for config in other_active_settings:
                if config.pk != self.pk:
                    config.is_active = False
                    config.save(update_fields=("is_active",))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Settings"
        verbose_name_plural = "Settings"


class News(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, verbose_name="Title", blank=True)
    description = models.TextField(verbose_name="Description", blank=True)
    link = models.URLField(verbose_name="Link", null=True, blank=True)
    published = models.CharField(max_length=255, verbose_name="Published", blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # technical fields
    last_update = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Additional info"
        verbose_name_plural = "Additional info"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    Profile.objects.get_or_create(user=instance)
    instance.profile.save()
