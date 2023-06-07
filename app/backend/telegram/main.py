from __future__ import annotations
from typing import TYPE_CHECKING
import telebot
from telebot import types
from backend.models import (
    BotSettings, PostBackEvent, TelegramUser,
    BotText, BotButton, BotStatus, BotError
)
from backend.enum import PostBackEventChoices
from .exceptions import (
    TokenNotFoundException
)

if TYPE_CHECKING:
    from telebot import TeleBot


class Messages:

    @staticmethod
    def _get_text(slug: str) -> str:
        bot_text = BotText.objects.filter(ident=slug).first()
        if bot_text:
            return bot_text.text
        return ""

    @property
    def settings(self) -> BotSettings:
        return BotSettings.get_solo()

    def get(self, code: str, **kwargs) -> str:
        _text = self._get_text(code)
        if hasattr(self, f"get_{code}"):
            return getattr(self, f"get_{code}")(text=_text, **kwargs)
        else:
            return _text

    def get_help(self, text):
        return text.format(
            self.settings.support_link,
        )

    def get_signup(self, text, **kwargs):
        message = kwargs.get("message")
        link = self.settings.site_link.format(
            message.from_user.id,
        )
        return text.format(link)

    def get_for_dep(self, text):
        link = self.settings.refill_link
        return text.format(link)

    def get_dep_check_success(self, text):
        link = self.settings.channel_link
        return text.format(link)

    def get_vip(self, text):
        link = self.settings.channel_link
        return text.format(link)


class Buttons:
    @staticmethod
    def _get_text(slug: str) -> str:
        bot_button = BotButton.objects.filter(ident=slug).first()
        if bot_button:
            return bot_button.text
        return ""

    def get_all_buttons(self) -> dict:
        buttons = BotButton.objects.all()
        result = dict()
        for button in buttons:
            result.update({
                button.ident: button.text
            })
        return result

    @property
    def signup_btn(self):
        return types.InlineKeyboardButton(self._get_text("signup"), callback_data="signup")

    @property
    def signup_check_btn(self):
        return types.InlineKeyboardButton(self._get_text("signup_check"), callback_data="signup_check")

    @property
    def help_btn(self):
        return types.InlineKeyboardButton(self._get_text("help"), callback_data="help")

    @property
    def back_btn(self):
        return types.InlineKeyboardButton(self._get_text("back"), callback_data="back_to_start")

    @property
    def back_to_dep_btn(self):
        return types.InlineKeyboardButton(self._get_text("back"), callback_data="back_to_dep_btn")

    @property
    def dep_btn(self):
        return types.InlineKeyboardButton(self._get_text("dep"), callback_data="dep")

    @property
    def check_dep_btn(self):
        return types.InlineKeyboardButton(self._get_text("check_dep"), callback_data="check_dep")

    @property
    def help_reply_btn(self):
        return types.KeyboardButton(self._get_text("help"))

    @property
    def signals_reply_btn(self):
        return types.KeyboardButton(self._get_text("signals"))

    @property
    def vip_reply_btn(self):
        return types.KeyboardButton(self._get_text("vip"))


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
    markup = types.InlineKeyboardMarkup()
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


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "signup":
        signup_action(call)
    elif call.data == "back_to_start":
        go_back_action(call)
    elif call.data == "signup_check":
        check_signup_action(call)
    elif call.data == "help":
        help_action(call)
    elif call.data == "dep":
        dep_action(call)
    elif call.data == "check_dep":
        check_dep_action(call)
    elif call.data == "back_to_dep_btn":
        back_to_dep_action(call)


def help_action(message) -> None:
    markup = types.InlineKeyboardMarkup()
    markup.add(Buttons.back_btn)
    bot.edit_message_text(
        chat_id=message.from_user.id, text=messages.get("help"), message_id=message.message.id,
        reply_markup=markup,
    )


def go_back_action(message) -> None:
    markup = types.InlineKeyboardMarkup()
    markup.add(Buttons.signup_btn, Buttons.signup_check_btn)
    markup.add(Buttons.help_btn)
    bot.edit_message_text(
        chat_id=message.from_user.id, text=messages.get("main"), message_id=message.message.id,
        reply_markup=markup,
    )


def signup_action(message) -> None:
    markup = types.InlineKeyboardMarkup()
    markup.add(Buttons.back_btn)
    bot.edit_message_text(
        chat_id=message.from_user.id, text=messages.get("signup", message=message), message_id=message.message.id,
        reply_markup=markup,
    )


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
    markup = types.InlineKeyboardMarkup()
    if events.exists():
        markup.add(Buttons.dep_btn)
        markup.add(Buttons.check_dep_btn)
        bot.edit_message_text(
            chat_id=message.from_user.id, text=messages.get("signup_success", message=message),
            message_id=message.message.id, reply_markup=markup,
        )
    else:
        markup.add(Buttons.back_btn)
        bot.edit_message_text(
            chat_id=message.from_user.id, text=messages.get("signup_failed", message=message),
            message_id=message.message.id, reply_markup=markup,
        )


def back_to_dep_action(message) -> None:
    markup = types.InlineKeyboardMarkup()
    markup.add(Buttons.dep_btn)
    markup.add(Buttons.check_dep_btn)
    bot.edit_message_text(
        chat_id=message.from_user.id, text=messages.get("signup_success", message=message),
        message_id=message.message.id, reply_markup=markup,
    )


def dep_action(message) -> None:
    markup = types.InlineKeyboardMarkup()
    markup.add(Buttons.back_to_dep_btn)
    bot.edit_message_text(
        chat_id=message.from_user.id, text=messages.get("for_dep"),
        message_id=message.message.id, reply_markup=markup,
    )


def check_dep_action(message) -> None:
    telegram_id = message.from_user.id
    events = PostBackEvent.objects.filter(
        event_type=PostBackEventChoices.DEP,
        sub1=telegram_id,
    )
    if events.count() >= 2:
        t = TelegramUser.objects.filter(telegram_id=message.from_user.id).first()
        if not t:
            markup = types.InlineKeyboardMarkup()
            markup.add(Buttons.back_to_dep_btn)
            bot.edit_message_text(
                chat_id=message.from_user.id, text=messages.get("dep_check_error", message=message),
                message_id=message.message.id, reply_markup=markup,
            )
        t.verified = True
        t.save(update_fields=("verified",))

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(Buttons.vip_reply_btn, Buttons.signals_reply_btn)
        markup.add(Buttons.help_reply_btn)

        bot.delete_message(
            chat_id=message.from_user.id, message_id=message.message.id,
        )
        bot.send_message(
            chat_id=message.from_user.id, text=messages.get("dep_check_success"), reply_markup=markup,
        )
    else:
        markup = types.InlineKeyboardMarkup()
        markup.add(Buttons.back_to_dep_btn)
        bot.edit_message_text(
            chat_id=message.from_user.id, text=messages.get("dep_check_error", message=message),
            message_id=message.message.id, reply_markup=markup,
        )


def help_reply_action(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(Buttons.vip_reply_btn, Buttons.signals_reply_btn)
    markup.add(Buttons.help_reply_btn)
    bot.send_message(
        chat_id=message.from_user.id, text=messages.get("help"), reply_markup=markup,
    )


def signals_reply_action(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(Buttons.vip_reply_btn, Buttons.signals_reply_btn)
    markup.add(Buttons.help_reply_btn)
    bot.send_message(
        chat_id=message.from_user.id, text=messages.get("signals"), reply_markup=markup,
    )


def vip_reply_action(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(Buttons.vip_reply_btn, Buttons.signals_reply_btn)
    markup.add(Buttons.help_reply_btn)
    bot.send_message(
        chat_id=message.from_user.id, text=messages.get("vip"), reply_markup=markup,
    )


@bot.message_handler(content_types=['text'])
def text_message(message) -> None:
    t = TelegramUser.objects.filter(telegram_id=message.from_user.id).first()
    if t and t.verified:
        buttons = Buttons.get_all_buttons()
        if message.text == buttons["help"]:
            help_reply_action(message)
        elif message.text == buttons["signals"]:
            signals_reply_action(message)
        elif message.text == buttons["vip"]:
            vip_reply_action(message)
        else:
            not_found_action(message)
    else:
        not_found_action(message)


def start_bot() -> None:
    bot_status = BotStatus.get_solo()
    bot_status.is_active = True
    bot_status.save(update_fields=("is_active",))
    try:
        bot.polling(none_stop=True, interval=0)
    except Exception as e:
        BotError.objects.create(
            text=e,
        )
        bot_status.is_active = False
        bot_status.save(update_fields=("is_active",))
        raise e
