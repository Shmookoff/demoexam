from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    UsernameField,
    AuthenticationForm as BaseAuthenticationForm,
)
from .models import Statements, User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import password_validation


class RegisterForm(UserCreationForm):
    full_name = forms.CharField(label="ФИО")
    phone = forms.RegexField(r"\+7\(\d\d\d\)-\d\d\d\s\d\d-\d\d", label="Телефон")

    password1 = forms.CharField(
        label=_("Пароль"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Подтверждение пароля"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    def save(self, commit: bool = True):
        user = super().save(commit=False)
        full_name = self.cleaned_data.get("full_name")
        user.full_name = full_name
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = [
            "username",
            "password1",
            "password2",
            "full_name",
            "phone",
            "email",
        ]
        labels = {
            "username": _("Логин"),
            "email": _("Адрес электронной почты"),
        }


class AuthenticationForm(BaseAuthenticationForm):
    username = UsernameField(
        label=_("Логин"), widget=forms.TextInput(attrs={"autofocus": True})
    )
    password = forms.CharField(
        label=_("Пароль"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )


class CreateStatementForm(forms.ModelForm):
    class Meta:
        model = Statements
        fields = [
            "car_registration_number",
            "description",
        ]
        labels = {
            "car_registration_number": _("Государственный регистрационный номер"),
            "description": _("Описание"),
        }
        widgets = {
            "description": forms.Textarea(),
        }


class StatementStatusForm(forms.ModelForm):
    class Meta:
        model = Statements
        fields = ["status"]
