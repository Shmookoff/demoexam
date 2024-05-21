from django.http import HttpRequest, QueryDict
from django.shortcuts import redirect, render
from django.contrib.auth.views import (
    LoginView as BaseLoginView,
    LogoutView as BaseLogoutView,
)
from django.contrib.auth.decorators import login_required
from app.forms import (
    AuthenticationForm,
    CreateStatementForm,
    RegisterForm,
    StatementStatusForm,
)
from app.models import Statement
from django.contrib.admin.views.decorators import staff_member_required


def register(request: HttpRequest):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})


class LoginView(BaseLoginView):
    form_class = AuthenticationForm
    template_name = "login.html"
    next_page = "statements"


class LogoutView(BaseLogoutView):
    next_page = "login"


@login_required
def statements(request: HttpRequest):
    statements = Statement.objects.filter(reporter=request.user).all()

    return render(request, "statements.html", {"statements": statements})


@login_required
def new_statement(request: HttpRequest):
    if request.method == "POST":
        form = CreateStatementForm(request.POST)
        if form.is_valid():
            statement = form.save(commit=False)
            statement.reporter = request.user
            statement.save()
            return redirect("statements")
    else:
        form = CreateStatementForm()

    return render(request, "new_statement.html", {"form": form})


@staff_member_required
def app_admin(request: HttpRequest):
    if request.method == "POST":
        update_statement_status(request.POST)

    form = StatementStatusForm()
    statements = Statement.objects.all()
    return render(request, "app_admin.html", {"statements": statements, "form": form})


def update_statement_status(POST: QueryDict):
    statement_id = POST.get("statement_id")
    form = StatementStatusForm(POST)
    if not (statement_id and form.is_valid()):
        return
    statement = Statement.objects.filter(id=statement_id).first()
    if not statement:
        return
    status = form.cleaned_data.get("status")
    if not status:
        return
    statement.status = status
    statement.save()
