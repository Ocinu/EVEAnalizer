import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from universe.models import Article, Region, SolarSystem


class Location(models.Model):
    eve_id = models.BigIntegerField(primary_key=True, editable=False)
    name = models.CharField(max_length=250, blank=True, default="Unnamed")
    type = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="locations",
        null=True,
    )
    solar_system = models.ForeignKey(
        SolarSystem, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return self.name


class Corporation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    eve_id = models.BigIntegerField(verbose_name="EVE ID", null=True, db_index=True)
    name = models.CharField(verbose_name="Name", max_length=250, blank=True)
    ticker = models.CharField(verbose_name="Corp ticker", max_length=250, blank=True)
    icon = models.URLField(verbose_name="icon", max_length=250, blank=True)

    def __str__(self):
        return self.name


class Character(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    corporation = models.ForeignKey(
        Corporation,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    location = models.ForeignKey(
        SolarSystem, on_delete=models.SET_NULL, null=True, blank=True
    )

    eve_id = models.BigIntegerField(verbose_name="EVE ID", null=True, db_index=True)
    name = models.CharField(verbose_name="Name", max_length=100, blank=True)
    birthday = models.DateField(
        verbose_name="birthday", auto_now_add=True, blank=True, null=True
    )
    portrait = models.URLField(verbose_name="Portrait", max_length=250, blank=True)
    wallet_balance = models.DecimalField(
        verbose_name="Wallet balance",
        max_digits=17,
        decimal_places=2,
        null=True,
        default=0,
    )
    total_sp = models.PositiveIntegerField(
        verbose_name="Total SP", null=True, default=0
    )

    # technical fields
    access_token = models.TextField(blank=True, default="")
    refresh_token = models.TextField(blank=True, default="")
    last_update = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ["pk"]


class MarketOrder(models.Model):
    class StatusChoices(models.TextChoices):
        CANCELLED = "cancelled", _("cancelled")
        EXPIRED = "expired", _("expired")
        OPEN = "open", _("open")
        COMPLETED = "completed", _("completed")

    order_id = models.BigIntegerField(null=True, default=0, unique=True, db_index=True)
    owner = models.ForeignKey(
        Character,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="orders",
    )
    article = models.ForeignKey(
        Article, on_delete=models.SET_NULL, null=True, blank=True, related_name="orders"
    )
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, null=True, blank=True, related_name="orders"
    )
    region = models.ForeignKey(
        Region, on_delete=models.CASCADE, null=True, blank=True, related_name="orders"
    )

    duration = models.PositiveIntegerField(null=True, default=0)
    escrow = models.DecimalField(max_digits=50, decimal_places=2, default=0, null=True)
    is_buy_order = models.BooleanField(default=False)
    is_corporation = models.BooleanField(default=False)
    issued = models.CharField(max_length=50, default="", blank=True)
    min_volume = models.PositiveIntegerField(null=True, default=0)
    price = models.DecimalField(max_digits=50, decimal_places=2, default=0)
    range = models.CharField(max_length=250, blank=True, default="")
    volume_remain = models.PositiveIntegerField(null=True, default=0)
    volume_total = models.PositiveIntegerField(null=True, default=0)

    state = models.CharField(
        max_length=250, choices=StatusChoices.choices, default=StatusChoices.OPEN
    )

    def __str__(self):
        return self.article.name
