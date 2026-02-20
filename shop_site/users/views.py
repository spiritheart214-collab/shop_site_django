from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import TemplateView


class HelloWorldView(TemplateView):
    """Временная страница. Для ридиректов и тестов"""

    template_name = "users/hello_world.html"


class UserLoginView(LoginView):
    """Вход пользователя"""
    template_name = "users/login.html"
    redirect_authenticated_user = True
    next_page = "users:hello_world"


class UserLogoutView(LogoutView):
    """Вход пользователя"""
    next_page = reverse_lazy("users:login")
