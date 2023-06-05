from django.contrib import admin
from .models import BotSettings, BotError, PostBackEvent
from solo.admin import SingletonModelAdmin


class BotErrorAdmin(admin.ModelAdmin):
    readonly_fields = (
        "text",
        "date",
    )

    def has_add_permission(self, request):
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


admin.site.register(BotSettings, SingletonModelAdmin)
admin.site.register(BotError, BotErrorAdmin)
admin.site.register(PostBackEvent, PostBackEventAdmin)
