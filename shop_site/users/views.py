from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.views.generic import TemplateView


class HelloWorldView(TemplateView):
    """Временная страница. Для ридиректов и тестов"""

    template_name = "users/hello_world.html"


class UserLogoutView(LogoutView):
    """Ралогирование пользователя"""
    next_page = reverse_lazy("users:login")
