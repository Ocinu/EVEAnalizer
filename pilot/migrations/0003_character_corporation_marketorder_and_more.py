# Generated by Django 4.2.3 on 2023-07-10 13:55

import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("universe", "0006_remove_article_market_group_id"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("pilot", "0002_remove_marketorder_article_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Character",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "eve_id",
                    models.BigIntegerField(
                        db_index=True, null=True, verbose_name="EVE ID"
                    ),
                ),
                (
                    "name",
                    models.CharField(blank=True, max_length=100, verbose_name="Name"),
                ),
                (
                    "birthday",
                    models.DateField(
                        auto_now_add=True, null=True, verbose_name="birthday"
                    ),
                ),
                (
                    "portrait",
                    models.URLField(
                        blank=True, max_length=250, verbose_name="Portrait"
                    ),
                ),
                (
                    "wallet_balance",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=17,
                        null=True,
                        verbose_name="Wallet balance",
                    ),
                ),
                (
                    "total_sp",
                    models.PositiveIntegerField(
                        default=0, null=True, verbose_name="Total SP"
                    ),
                ),
                ("access_token", models.TextField(blank=True, default="")),
                ("refresh_token", models.TextField(blank=True, default="")),
                ("last_update", models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                "ordering": ["pk"],
            },
        ),
        migrations.CreateModel(
            name="Corporation",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "eve_id",
                    models.BigIntegerField(
                        db_index=True, null=True, verbose_name="EVE ID"
                    ),
                ),
                (
                    "name",
                    models.CharField(blank=True, max_length=250, verbose_name="Name"),
                ),
                (
                    "ticker",
                    models.CharField(
                        blank=True, max_length=250, verbose_name="Corp ticker"
                    ),
                ),
                (
                    "icon",
                    models.URLField(blank=True, max_length=250, verbose_name="icon"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="MarketOrder",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "order_id",
                    models.BigIntegerField(
                        db_index=True, default=0, null=True, unique=True
                    ),
                ),
                ("duration", models.PositiveIntegerField(default=0, null=True)),
                (
                    "escrow",
                    models.DecimalField(
                        decimal_places=2, default=0, max_digits=50, null=True
                    ),
                ),
                ("is_buy_order", models.BooleanField(default=False)),
                ("is_corporation", models.BooleanField(default=False)),
                ("issued", models.CharField(blank=True, default="", max_length=50)),
                ("min_volume", models.PositiveIntegerField(default=0, null=True)),
                (
                    "price",
                    models.DecimalField(decimal_places=2, default=0, max_digits=50),
                ),
                ("range", models.CharField(blank=True, default="", max_length=250)),
                ("volume_remain", models.PositiveIntegerField(default=0, null=True)),
                ("volume_total", models.PositiveIntegerField(default=0, null=True)),
                (
                    "state",
                    models.CharField(
                        choices=[
                            ("cancelled", "cancelled"),
                            ("expired", "expired"),
                            ("open", "open"),
                            ("completed", "completed"),
                        ],
                        default="open",
                        max_length=250,
                    ),
                ),
                (
                    "article",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="orders",
                        to="universe.article",
                    ),
                ),
                (
                    "location",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="orders",
                        to="pilot.location",
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="orders",
                        to="pilot.character",
                    ),
                ),
                (
                    "region",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="orders",
                        to="universe.region",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="character",
            name="corporation",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="pilot.corporation",
            ),
        ),
        migrations.AddField(
            model_name="character",
            name="location",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="universe.solarsystem",
            ),
        ),
        migrations.AddField(
            model_name="character",
            name="owner",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
