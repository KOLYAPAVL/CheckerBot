from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import BotMessage, TelegramUser
from backend.telegram.utils import send_message


@receiver(post_save, sender=BotMessage)
def on_create_bot_message(sender, created, instance, **kwargs) -> None:
    if created:
        users = instance.users.all()
        if users.count() == 0:
            users = TelegramUser.objects.filter(verified=True)

        chat_ids = list(users.values_list("telegram_id", flat=True))
        send_message(chat_ids, instance.text)
