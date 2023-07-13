from django.contrib import admin

from .models import Character, Corporation, Location, MarketOrder


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = (
        "eve_id",
        "name",
        "total_sp",
        "wallet_balance",
    )
    list_display_links = (
        "eve_id",
        "name",
        "total_sp",
        "wallet_balance",
    )
    readonly_fields = (
        "access_token",
        "refresh_token",
        "last_update",
        "eve_id",
        "name",
        "total_sp",
        "wallet_balance",
    )


@admin.register(Corporation)
class CorporationAdmin(admin.ModelAdmin):
    list_display = ("eve_id", "name")


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("eve_id", "name", "type", "solar_system")
    search_fields = ("eve_id", "name")
    readonly_fields = ("eve_id", "name", "type", "solar_system")


@admin.register(MarketOrder)
class MarketOrderAdmin(admin.ModelAdmin):
    list_display = (
        "article",
        "location",
        "region",
        "is_buy_order",
        "volume_total",
        "volume_remain",
        "price",
        "state",
    )
    search_fields = (
        "article",
        "location",
        "region",
    )
    list_filter = ("is_buy_order", "state")
