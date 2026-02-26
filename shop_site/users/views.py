from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView

from .models import User
from .forms import UserRegistrationsForm, UserUpdateForm, UserUpdatePasswordForm
from .views_mixin import UserAccessMixin, UserSuccessUrlMixin


class UserRegistrationView(UserSuccessUrlMixin, CreateView):
    """Регистрация пользователя"""
    form_class = UserRegistrationsForm
    template_name = "users/register.html"

    def form_valid(self, form: UserRegistrationsForm):
        """Автоматический логин после регистрации"""

        response = super().form_valid(form)
        login(self.request, self.object)

        return response


class UserLoginView(UserSuccessUrlMixin, LoginView):
    """Вход пользователя"""
    template_name = "users/login.html"
    redirect_authenticated_user = True


class UserLogoutView(LogoutView):
    """Вход пользователя"""
    next_page = reverse_lazy("users:login")


class UserDetailView(LoginRequiredMixin, UserAccessMixin, DetailView):
    """Страница пользователя"""
    template_name = "users/user_detail.html"
    model = User
    context_object_name = "user"


class UserUpdateView(LoginRequiredMixin, UserAccessMixin, UserSuccessUrlMixin, UpdateView):
    """Страница обновления пользователя"""
    template_name = "users/user_update.html"
    model = User
    form_class = UserUpdateForm


class UserUpdatePasswordView(LoginRequiredMixin, UserSuccessUrlMixin, PasswordChangeView):
    """Страница обновления пороля"""
    template_name = "users/user_update_password.html"
    form_class = UserUpdatePasswordForm
