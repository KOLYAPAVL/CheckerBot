from django.db import models
from django.utils.translation import gettext_lazy as l_
from solo.models import SingletonModel
from .enum import PostBackEventChoices


# Create your models here.
class BotSettings(SingletonModel):

    support_link = models.CharField(
        verbose_name=l_("Ссылка по поддержку"),
        blank=False,
        default="",
        max_length=128,
    )
    site_link = models.CharField(
        verbose_name=l_("Ссылка на сайт"),
        blank=False,
        default="",
        max_length=128,
    )
    refill_link = models.CharField(
        verbose_name=l_("Ссылка для пополнения"),
        blank=True,
        default="",
        max_length=128,
    )
    channel_link = models.CharField(
        verbose_name=l_("Ссылка на канал"),
        blank=True,
        default="",
        max_length=128,
    )
    bot_token = models.TextField(
        verbose_name=l_("Токен бота"),
        blank=False,
        default="",
    )

    class Meta:
        verbose_name = l_("Настройки бота")

    def __str__(self):
        return "Настройки бота"


class BotError(models.Model):
    text = models.TextField(
        verbose_name=l_("Лог"),
    )
    date = models.DateTimeField(
        verbose_name=l_("Дата создания"),
        auto_now_add=True,
    )

    class Meta:
        verbose_name = l_("Ошибка бота")
        verbose_name_plural = l_("Ошибки бота")

    def __str__(self):
        return f"Ошибка: {self.text}"


class PostBackEvent(models.Model):

    event_type = models.PositiveSmallIntegerField(
        verbose_name=l_("Вид события"),
        choices=PostBackEventChoices.choices,
        default=PostBackEventChoices.SIGNUP,
        blank=False,
    )
    event_id = models.CharField(
        verbose_name=l_("Event Id"),
        max_length=128,
        blank=False,
        default="",
    )
    date = models.DateTimeField(
        verbose_name=l_("Дата события"),
        auto_now_add=True,
    )
    amount = models.FloatField(
        verbose_name=l_("Сумма"),
        blank=True,
        null=True,
    )
    country = models.CharField(
        verbose_name=l_("Страна"),
        max_length=128,
        blank=True,
        default="",
    )
    user_id = models.CharField(
        verbose_name=l_("User Id"),
        max_length=128,
        blank=False,
        default="",
    )
    sub1 = models.CharField(
        verbose_name=l_("Sub1"),
        max_length=128,
        blank=False,
        default="",
    )

    class Meta:
        verbose_name = l_("PostBack событие")
        verbose_name_plural = l_("PostBack события")

    def __str__(self):
        return f"Postback event #{self.id}"


class BotMessage(models.Model):

    text = models.TextField(
        verbose_name=l_("Текст сообщения"),
    )
    users = models.ManyToManyField(
        "TelegramUser",
        verbose_name=l_("Адресаты"),
        blank=True,
        help_text=l_("Если адресата оставить пустым, сообщение "
                     "уйдет всем пользователям бота")
    )
    date = models.DateTimeField(
        verbose_name=l_("Дата создания"),
        auto_now_add=True
    )

    class Meta:
        verbose_name = l_("Сообщение в бота")
        verbose_name_plural = l_("Сообщения в бота")

    def __str__(self):
        return f"Сообщение в бота {self.id}"


class TelegramUser(models.Model):

    telegram_id = models.CharField(
        verbose_name=l_("Telegram Id"),
        blank=False,
        max_length=64,
        default="",
    )
    name = models.CharField(
        verbose_name=l_("Имя"),
        blank=False,
        max_length=256,
        default="",
    )
    username = models.CharField(
        verbose_name=l_("Имя пользователя Telegram"),
        blank=False,
        max_length=256,
        default="",
        help_text="t.me/@<имя пользователя>"
    )
    verified = models.BooleanField(
        verbose_name=l_("Верификация пройдена"),
        default=False,
    )

    class Meta:
        verbose_name = l_("Telegram пользователь")
        verbose_name_plural = l_("Telegram пользователи")

    def __str__(self):
        return f"Пользователь #{self.telegram_id}"


class BotStatus(SingletonModel):
    is_active = models.BooleanField(
        verbose_name=l_("Активный"),
        default=False,
    )

    class Meta:
        verbose_name = l_("Статус бота")

    def __str__(self):
        return "Статус бота"


class BotText(models.Model):

    ident = models.SlugField(
        unique=True,
        verbose_name=l_("Идентификатор сообщения"),
        blank=False,
        max_length=128,
    )
    text = models.TextField(
        verbose_name=l_("Текст"),
        max_length=128,
    )

    class Meta:
        verbose_name = l_("Текст бота")
        verbose_name_plural = l_("Тексты бота")

    def __str__(self):
        return f"Текст бота: {self.text}"


class BotButton(models.Model):

    ident = models.SlugField(
        unique=True,
        verbose_name=l_("Идентификатор кнопки"),
        blank=False,
        max_length=128,
    )
    text = models.TextField(
        verbose_name=l_("Текст"),
        max_length=128,
    )

    class Meta:
        verbose_name = l_("Кнопка бота")
        verbose_name_plural = l_("Кнопки бота")

    def __str__(self):
        return f"Кнопка бота: {self.text}"
