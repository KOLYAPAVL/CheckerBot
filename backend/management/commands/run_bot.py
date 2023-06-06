from backend.telegram.main import start_bot
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Запуск бота'

    def handle(self, *args, **options):
        start_bot()
