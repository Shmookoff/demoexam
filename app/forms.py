from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm as BaseAuthenticationForm,
)
from .models import Statement, User


class RegisterForm(UserCreationForm):
    full_name = forms.CharField(label="ФИО")

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


class AuthenticationForm(BaseAuthenticationForm):
    pass


class CreateStatementForm(forms.ModelForm):
    class Meta:
        model = Statement
        fields = [
            "car_registration_number",
            "description",
            "date_time",
        ]
        widgets = {
            "description": forms.Textarea(),
            "date_time": forms.DateTimeInput({"type": "datetime-local"}),
        }


class StatementStatusForm(forms.ModelForm):
    forms.DateTimeField

    class Meta:
        model = Statement
        fields = ["status"]
