from django.contrib import admin

from .models import (Article, Category, Constellation, Group, Region,
                     SolarSystem)


@admin.register(SolarSystem)
class SolarSystemAdmin(admin.ModelAdmin):
    list_display = ("eve_id", "name", "constellation", "security_status")
    search_fields = ("eve_id", "name")
    readonly_fields = ("eve_id", "name", "constellation", "security_status")
    list_display_links = ("eve_id", "name")


@admin.register(Constellation)
class ConstellationAdmin(admin.ModelAdmin):
    list_display = ("eve_id", "name", "region")
    search_fields = ("eve_id", "name")
    readonly_fields = ("eve_id", "name", "region")
    list_display_links = ("eve_id", "name")


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ("eve_id", "name")
    search_fields = ("eve_id", "name")
    readonly_fields = ("eve_id", "name")
    list_display_links = ("eve_id", "name")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("eve_id", "name")
    search_fields = ("eve_id", "name")
    readonly_fields = ("eve_id", "name")
    list_display_links = ("eve_id", "name")


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("eve_id", "name", "category")
    search_fields = ("eve_id", "name", "category__name")
    readonly_fields = ("eve_id", "name", "category")
    list_display_links = ("eve_id", "name")


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        "eve_id",
        "name",
        "group",
        "published",
        "packaged_volume",
        "average_price",
        "icon_url",
    )
    search_fields = (
        "eve_id",
        "name",
        "group__name",
    )
    readonly_fields = (
        "eve_id",
        "name",
        "group",
        "published",
        "packaged_volume",
        "volume",
    )
    list_display_links = ("eve_id", "name", "packaged_volume", "average_price")
    list_filter = ("published",)
