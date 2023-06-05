from __future__ import annotations
from typing import TYPE_CHECKING
import telebot
from telebot import types
from backend.models import BotSettings
from .exceptions import (
    TokenNotFoundException
)

if TYPE_CHECKING:
    from telebot import TeleBot


settings = BotSettings.get_solo()


class Messages:
    main = "👇 Выберите раздел меню"
    help = "🆘 Для помощи обратитесь к этому человеку {}"
    signup = "🔗 Ссылка для регистрации {}"
    not_found = "🟥 Комманда не найдена"

    def get(self, code: str, **kwargs) -> str:
        if hasattr(self, f"get_{code}"):
            return getattr(self, f"get_{code}")(**kwargs)
        else:
            return getattr(self, code)

    def get_help(self):
        return self.help.format(
            settings.support_link,
        )

    def get_signup(self, **kwargs):
        message = kwargs.get("message")
        link = settings.site_link.format(
            message.from_user.id,
        )
        return self.signup.format(link)


class Buttons:
    signup = "🎟 Регистрация"
    signup_check = "✅ Проверить регистрацию"
    help = "ℹ️ Помощь"
    back = "🔙 Назад"

    @property
    def signup_btn(self):
        return types.KeyboardButton(self.signup)

    @property
    def signup_check_btn(self):
        return types.KeyboardButton(self.signup_check)

    @property
    def help_btn(self):
        return types.KeyboardButton(self.help)

    @property
    def back_btn(self):
        return types.KeyboardButton(self.back)


def get_bot() -> TeleBot:
    if not settings.bot_token:
        raise TokenNotFoundException("Токен не найден")
    _bot_instance = telebot.TeleBot(settings.bot_token)
    return _bot_instance


bot = get_bot()
messages = Messages()
Buttons = Buttons()


def main_action(message) -> None:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(Buttons.signup_btn, Buttons.signup_check_btn)
    markup.add(Buttons.help_btn)
    bot.send_message(message.from_user.id, messages.get("main"), reply_markup=markup)


@bot.message_handler(commands=['start'])
def start(message) -> None:
    main_action(message)


def help_action(message) -> None:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(Buttons.back_btn)
    bot.send_message(message.from_user.id, messages.get("help"), reply_markup=markup)


def signup_action(message) -> None:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(Buttons.back_btn)
    bot.send_message(message.from_user.id, messages.get("signup", message=message), reply_markup=markup)


def not_found_action(message) -> None:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(Buttons.back_btn)
    bot.send_message(message.from_user.id, messages.get("not_found"), reply_markup=markup)


def check_signup_action(message) -> None:
    ...


@bot.message_handler(content_types=['text'])
def text_message(message) -> None:
    if message.text == Buttons.signup:
        signup_action(message)
    elif message.text == Buttons.help:
        help_action(message)
    elif message.text == Buttons.back:
        main_action(message)
    elif message.text == Buttons.signup_check:
        check_signup_action(message)
    else:
        not_found_action(message)


def start_bot() -> None:
    bot.polling(none_stop=True, interval=0)
