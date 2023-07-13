from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import News, Profile, Settings


@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "client_id", "secret_key", "is_active")
    list_display_links = (
        "id",
        "name",
        "client_id",
        "secret_key",
    )
    readonly_fields = ("base64_key",)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "link",
        "published",
    )
    readonly_fields = ("id",)


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "profile"

    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in self.model._meta.fields]


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
