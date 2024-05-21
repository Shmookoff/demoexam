from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    first_name = models.CharField(
        max_length=150,
        null=False,
        blank=False,
    )
    middle_name = models.CharField(max_length=150, null=False, blank=False)
    last_name = models.CharField(max_length=150, null=False, blank=False)
    phone = models.CharField(max_length=30, null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False)

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


class Statements(models.Model):
    class Status(models.TextChoices):
        NEW = "N", _("Новое")
        APPROVED = "A", _("Подтверждено")
        REJECTED = "R", _("Отклонено")

    car_registration_number = models.CharField(max_length=15, blank=False)
    description = models.CharField(max_length=300, blank=False)
    status = models.CharField(max_length=1, choices=Status, default=Status.NEW)
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
