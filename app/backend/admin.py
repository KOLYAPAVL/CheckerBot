from django.contrib import admin
from .models import (
    BotSettings, BotError, PostBackEvent,
    BotMessage, TelegramUser, BotStatus, BotText,
    BotButton,
)
from solo.admin import SingletonModelAdmin
from django_object_actions import DjangoObjectActions, action
from threading import Thread


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


class BotStatusAdmin(DjangoObjectActions, SingletonModelAdmin):

    @action(label="Запуск бота", description="Run bot")
    def run_bot(self, request, obj):
        try:
            from backend.telegram.main import start_bot
            thread = Thread(target=start_bot)
            thread.start()
        except:
            pass

    change_actions = ('run_bot',)

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False


class BotTextAdmin(admin.ModelAdmin):

    def has_delete_permission(self, request, obj=None):
        return False


class BotButtonAdmin(admin.ModelAdmin):

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(BotSettings, SingletonModelAdmin)
admin.site.register(BotError, BotErrorAdmin)
admin.site.register(PostBackEvent, PostBackEventAdmin)
admin.site.register(BotMessage, BotMessageAdmin)
admin.site.register(TelegramUser, TelegramUserAdmin)
admin.site.register(BotStatus, BotStatusAdmin)
admin.site.register(BotText, BotTextAdmin)
admin.site.register(BotButton, BotButtonAdmin)
