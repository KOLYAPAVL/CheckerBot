from django.db.models import IntegerChoices
from django.utils.translation import gettext_lazy as l_


class PostBackEventChoices(IntegerChoices):
    SIGNUP = 0, l_("Регистрация")
    FIRST_DEP = 1, l_("Первый депозит")
    DEP = 2, l_("Депозит")
