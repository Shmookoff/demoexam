from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm
from .models import Statement, User


class UserChangeForm(BaseUserChangeForm):
    class Meta(BaseUserChangeForm.Meta):
        model = User


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm

    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {"fields": ("middle_name", "phone")}),
    )


admin.site.register(User, UserAdmin)
admin.site.register(Statement)
