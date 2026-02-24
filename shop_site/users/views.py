from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from .models import User
from .forms import UserRegistrationsForm


class UserRegistrationView(CreateView):
    """Регистрация пользователя"""
    form_class = UserRegistrationsForm
    template_name = "users/register.html"

    def form_valid(self, form: UserRegistrationsForm):
        """Автоматический логин после регистрации"""

        user = form.save()
        login(self.request, user)

        return super().form_valid(form)

    def get_success_url(self):
        """Редирект на страницу о пользователе (UserDetailView)"""
        url = reverse_lazy("users:user", kwargs={"pk": self.object.pk})
        return url


class UserLoginView(LoginView):
    """Вход пользователя"""
    template_name = "users/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        """Редирект на страницу о пользователе (UserDetailView)"""
        url = reverse_lazy("users:user", kwargs={"pk": self.request.user.pk})
        return url


class UserLogoutView(LogoutView):
    """Вход пользователя"""
    next_page = reverse_lazy("users:login")


class UserDetailView(DetailView):
    """Страница пользователя"""
    template_name = "users/user_detail.html"
    model = User
