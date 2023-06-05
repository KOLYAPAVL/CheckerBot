from backend.models import BotError
from abc import ABC, abstractmethod


class BaseBotException(ABC, Exception):
    error_model_class = BotError

    @abstractmethod
    def get_message(self, message: str) -> str:
        return ""

    def __init__(self, message, *args, **kwargs):
        self.message = self.get_message(message)
        self.create_error_log()
        super().__init__(message, *args, **kwargs)

    def create_error_log(self):
        self.error_model_class.objects.create(
            text=self.message,
        )


class TokenNotFoundException(BaseBotException):

    def get_message(self, message: str) -> str:
        return "Токен бота не найден."
