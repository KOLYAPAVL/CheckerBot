from django.contrib import admin
from .models import (
    BotSettings, BotError, PostBackEvent,
    BotMessage, TelegramUser, BotStatus,
)
from solo.admin import SingletonModelAdmin


class BotErrorAdmin(admin.ModelAdmin):
    readonly_fields = (
        "text",
        "date",
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class PostBackEventAdmin(admin.ModelAdmin):
    readonly_fields = (
        "event_type",
        "event_id",
        "date",
        "amount",
        "country",
        "user_id",
        "sub1",
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class BotMessageAdmin(admin.ModelAdmin):
    readonly_fields = (
        "date",
    )
    raw_id_fields = (
        "users",
    )

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class TelegramUserAdmin(admin.ModelAdmin):

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False


class BotStatusAdmin(SingletonModelAdmin):

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False


admin.site.register(BotSettings, SingletonModelAdmin)
admin.site.register(BotError, BotErrorAdmin)
admin.site.register(PostBackEvent, PostBackEventAdmin)
admin.site.register(BotMessage, BotMessageAdmin)
admin.site.register(TelegramUser, TelegramUserAdmin)
admin.site.register(BotStatus, BotStatusAdmin)
