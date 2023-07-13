from django.db import models
from django.utils.translation import gettext_lazy as _


class Region(models.Model):
    class StatusChoices(models.TextChoices):
        HI_SEC = "hi_sec", _("hi security")
        LOW_SEC = "low_sec", _("low security")
        NULL_SEC = "null_sec", _("null security")

    eve_id = models.PositiveIntegerField(primary_key=True, editable=False)
    name = models.CharField(max_length=250, blank=True)
    trade_rout = models.CharField(
        max_length=250, choices=StatusChoices.choices, default=StatusChoices.NULL_SEC
    )

    def __str__(self):
        return self.name


class Constellation(models.Model):
    eve_id = models.PositiveIntegerField(primary_key=True, editable=False)
    name = models.CharField(max_length=250, blank=True)
    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="constellations",
    )

    def __str__(self):
        return self.name


class SolarSystem(models.Model):
    eve_id = models.PositiveIntegerField(primary_key=True, editable=False)
    name = models.CharField(max_length=250, blank=True)
    security_status = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    constellation = models.ForeignKey(
        Constellation,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="systems",
    )

    def __str__(self):
        return self.name


class Category(models.Model):
    eve_id = models.PositiveIntegerField(primary_key=True, editable=False)
    name = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return self.name


class Group(models.Model):
    eve_id = models.PositiveIntegerField(primary_key=True, editable=False)
    name = models.CharField(max_length=250, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, blank=True, related_name="groups"
    )

    def __str__(self):
        return self.name


class Article(models.Model):
    eve_id = models.PositiveIntegerField(primary_key=True, editable=False)
    name = models.CharField(max_length=250, blank=True, verbose_name="Name")
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Group",
        related_name="articles",
    )
    description = models.TextField(blank=True, verbose_name="Description")
    published = models.BooleanField(default=True, verbose_name="Published")
    packaged_volume = models.DecimalField(
        max_digits=20, decimal_places=6, null=True, verbose_name="Packaged volume"
    )
    volume = models.DecimalField(
        max_digits=20, decimal_places=6, null=True, verbose_name="Volume"
    )
    adjusted_price = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0,
        null=True,
        verbose_name="Adjusted price",
    )
    average_price = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0,
        null=True,
        verbose_name="Average price",
    )
    icon_url = models.URLField(verbose_name="icon", max_length=250, default="")
    render_url = models.URLField(verbose_name="picture", max_length=250, default="")

    def __str__(self):
        return self.name
