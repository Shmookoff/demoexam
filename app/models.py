from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator


class User(AbstractUser):
    first_name = models.CharField(
        _("first name"),
        max_length=150,
        null=False,
        blank=False,
    )
    middle_name = models.CharField("Отчество", max_length=150, null=False, blank=False)
    last_name = models.CharField(
        _("last name"), max_length=150, null=False, blank=False
    )
    phone = models.CharField(
        "Телефон",
        max_length=30,
        null=False,
        blank=False,
        validators=[
            RegexValidator(
                regex=r"\+7\(\d\d\d\)-\d\d\d-\d\d-\d\d",
                message="Введите телефон в формате +7(XXX)-XXX-XX-XX",
                code="invalid_phone_number",
            ),
        ],
    )
    email = models.EmailField(_("email address"), unique=True, null=False, blank=False)

    REQUIRED_FIELDS = ["first_name", "middle_name", "last_name", "phone", "email"]

    @property
    def full_name(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}"

    @full_name.setter
    def full_name(self, value: str):
        names = value.split(" ")
        self.last_name = names[0]
        self.first_name = names[1]
        self.middle_name = names[2]


def statement_date_time_only_hours(value: datetime):
    if value.minute or value.second or value.microsecond:
        raise ValidationError("Разрешается запись только по часам")


class Statement(models.Model):
    class Status(models.TextChoices):
        NEW = "N", _("Новое")
        APPROVED = "A", _("Подтверждено")
        REJECTED = "R", _("Отклонено")

    car_registration_number = models.CharField(
        "Государственный регистрационный номер", max_length=15, blank=False
    )
    description = models.CharField("Описание", max_length=300, blank=False)
    status = models.CharField(
        "Статус", max_length=1, choices=Status, default=Status.NEW
    )
    reporter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=False,
        verbose_name="Заявитель",
    )
    date_time = models.DateTimeField(
        "Дата и время", blank=False, validators=[statement_date_time_only_hours]
    )
