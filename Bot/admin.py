from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import BotConfig


class BotConfigAdmin(admin.ModelAdmin):
    list_display = ("title", "link", "token", "server_url", "is_active")
    list_display_links = ("title", "link", "token")
    search_fields = ("title",)


admin.site.register(BotConfig, BotConfigAdmin)
admin.site.site_header = mark_safe(
    '<img src="https://alpha-bots.com/wp-content/uploads/2020/08/logo-%E2%80%94-%D0%BA%D0%BE%D0%BF%D0%B8%D1%8F-2.png">'
)
