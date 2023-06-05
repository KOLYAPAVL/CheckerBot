from __future__ import annotations
from typing import TYPE_CHECKING
import telebot
from telebot import types
from backend.models import BotSettings, PostBackEvent, TelegramUser
from backend.enum import PostBackEventChoices
from .exceptions import (
    TokenNotFoundException
)

if TYPE_CHECKING:
    from telebot import TeleBot


class Messages:
    main = "👇 Выберите раздел меню"
    help = "🆘 Для помощи обратитесь к этому человеку {}"
    signup = "🔗 Ссылка для регистрации {}"
    not_found = "🟥 Комманда не найдена"
    signup_failed = "💧 Неудалось проверить регистрацию. Попробуйте позже"
    signup_success = "⭐ Регистрация успешно пройдена. Пополните баланс"
    for_dep = "🔗 Для пополнения перейдите по ссылке {}"
    dep_check_error = "💧 Пополнения не найдены"
    dep_check_success = ("""
⭐ Вы успешно пополнили баланс
🔗 Ссылка на канал {}
    """)

    def get(self, code: str, **kwargs) -> str:
        if hasattr(self, f"get_{code}"):
            return getattr(self, f"get_{code}")(**kwargs)
        else:
            return getattr(self, code)

    def get_help(self):
        settings = BotSettings.get_solo()
        return self.help.format(
            settings.support_link,
        )

    def get_signup(self, **kwargs):
        settings = BotSettings.get_solo()
        message = kwargs.get("message")
        link = settings.site_link.format(
            message.from_user.id,
        )
        return self.signup.format(link)

    def get_for_dep(self, **kwargs):
        settings = BotSettings.get_solo()
        link = settings.refill_link
        return self.for_dep.format(link)

    def get_dep_check_success(self):
        settings = BotSettings.get_solo()
        link = settings.channel_link
        return self.dep_check_success.format(link)


class Buttons:
    signup = "🎟 Регистрация"
    signup_check = "✅ Проверить регистрацию"
    help = "ℹ️ Помощь"
    back = "🔙 Назад"
    dep = "💰 Пополнить"
    check_dep = "💵 Проверить пополнение"

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

    @property
    def dep_btn(self):
        return types.KeyboardButton(self.dep)

    @property
    def check_dep_btn(self):
        return types.KeyboardButton(self.check_dep)


def get_bot() -> TeleBot:
    settings = BotSettings.get_solo()
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
    bot.send_message(message.from_user.id, messages.get("main"),
                     reply_markup=markup)


def assign_user(message) -> None:
    if TelegramUser.objects.filter(
        telegram_id=message.from_user.id,
    ).exists():
        return None
    TelegramUser.objects.create(
        telegram_id=message.from_user.id,
        name="{} {}".format(
            message.from_user.first_name, message.from_user.last_name
        ),
        username=message.from_user.username,
    )


@bot.message_handler(commands=['start'])
def start(message) -> None:
    assign_user(message)
    main_action(message)


def help_action(message) -> None:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(Buttons.back_btn)
    bot.send_message(message.from_user.id, messages.get("help"),
                     reply_markup=markup)


def signup_action(message) -> None:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(Buttons.back_btn)
    bot.send_message(message.from_user.id,
                     messages.get("signup", message=message),
                     reply_markup=markup)


def not_found_action(message) -> None:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(Buttons.back_btn)
    bot.send_message(message.from_user.id, messages.get("not_found"),
                     reply_markup=markup)


def check_signup_action(message) -> None:
    telegram_id = message.from_user.id
    events = PostBackEvent.objects.filter(
        event_type=PostBackEventChoices.SIGNUP,
        sub1=telegram_id,
    )
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if events.exists():
        markup.add(Buttons.dep_btn)
        markup.add(Buttons.check_dep_btn)
        bot.send_message(message.from_user.id,
                         messages.get("signup_success"),
                         reply_markup=markup)
    else:
        markup.add(Buttons.back_btn)
        bot.send_message(message.from_user.id,
                         messages.get("signup_failed"),
                         reply_markup=markup)


def dep_action(message) -> None:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(Buttons.dep_btn)
    markup.add(Buttons.check_dep_btn)
    bot.send_message(message.from_user.id,
                     messages.get("for_dep"),
                     reply_markup=markup)


def check_dep_action(message) -> None:
    telegram_id = message.from_user.id
    events = PostBackEvent.objects.filter(
        event_type=PostBackEventChoices.DEP,
        sub1=telegram_id,
    )
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if events.count() >= 2:
        markup.add(Buttons.dep_btn)
        bot.send_message(message.from_user.id,
                         messages.get("dep_check_success"),
                         reply_markup=markup)
    else:
        markup.add(Buttons.dep_btn)
        markup.add(Buttons.check_dep_btn)
        bot.send_message(message.from_user.id,
                         messages.get("dep_check_error"),
                         reply_markup=markup)


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
    elif message.text == Buttons.dep:
        dep_action(message)
    elif message.text == Buttons.check_dep:
        check_dep_action(message)
    else:
        not_found_action(message)


def start_bot() -> None:
    bot.polling(none_stop=True, interval=0)
