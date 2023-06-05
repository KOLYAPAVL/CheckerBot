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
