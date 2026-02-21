from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from .forms import UserRegistrationsForm


class HelloWorldView(TemplateView):
    """Временная страница. Для ридиректов и тестов"""
    template_name = "users/hello_world.html"


class UserRegistrationView(CreateView):
    """Регистрация пользователя"""
    form_class = UserRegistrationsForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:hello_world")

    def form_valid(self, form: UserRegistrationsForm):
        """Автоматический логин после регистрации"""

        user = form.save()
        login(self.request, user)

        return super().form_valid(form)


class UserLoginView(LoginView):
    """Вход пользователя"""
    template_name = "users/login.html"
    redirect_authenticated_user = True
    next_page = "users:hello_world"


class UserLogoutView(LogoutView):
    """Вход пользователя"""
    next_page = reverse_lazy("users:login")

# Todo сделать страницу пользователя вместо HelloWorldView

