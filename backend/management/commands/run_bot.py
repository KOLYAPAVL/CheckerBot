from backend.telegram.main import start_bot
from django.core.management.base import BaseCommand
from backend.models import BotStatus, BotError


class Command(BaseCommand):
    help = 'Запуск бота'

    def handle(self, *args, **options):
        bot_status = BotStatus.get_solo()
        bot_status.is_active = True
        bot_status.save(update_fields=("is_active",))
        try:
            start_bot()
        except Exception as e:
            BotError.objects.create(
                text=e,
            )
            bot_status.is_active = False
            bot_status.save(update_fields=("is_active",))
