from __future__ import annotations
import requests

from backend.models import BotSettings


def send_message(chat_ids: list, message: str) -> None:
    bot_settings = BotSettings.get_solo()
    for chat_id in chat_ids:
        send_text = (
            'https://api.telegram.org/bot{token}/sendMessage?'
            'chat_id={chat_id}&parse_mode=Markdown&text={message}'
        ).format(
            token=bot_settings.bot_token,
            chat_id=chat_id,
            message=message
        )
        requests.get(send_text)
