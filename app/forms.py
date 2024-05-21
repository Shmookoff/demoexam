from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm as BaseAuthenticationForm,
)
from .models import Statements, User


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
        model = Statements
        fields = [
            "car_registration_number",
            "description",
        ]
        widgets = {
            "description": forms.Textarea(),
        }


class StatementStatusForm(forms.ModelForm):
    class Meta:
        model = Statements
        fields = ["status"]
