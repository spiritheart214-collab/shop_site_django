from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView

from .models import User
from .forms import UserRegistrationsForm, UserUpdateForm


class UserRegistrationView(CreateView):
    """Регистрация пользователя"""
    form_class = UserRegistrationsForm
    template_name = "users/register.html"

    def form_valid(self, form: UserRegistrationsForm):
        """Автоматический логин после регистрации"""

        response = super().form_valid(form)
        login(self.request, self.object)

        return response

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


class UserDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """Страница пользователя"""
    template_name = "users/user_detail.html"
    model = User
    context_object_name = "user"

    def test_func(self):
        """
        Страницу может посетить:
         - пользователь
         - суперпользователь
         - стафф
        """

        user_page_owner: User = self.get_object()
        user_request: User = self.request.user

        can_see_the_page: bool = (user_request.is_superuser or
                                  user_request.is_staff or
                                  user_request == user_page_owner)

        if can_see_the_page:
            return True
        return False

    def handle_no_permission(self):
        """Если нет доступа, то вывод сообщения"""
        messages.error(request=self.request, message="У вас нет доступа к этой странице!")

        if self.request.user.is_authenticated:
            return redirect("users:user", pk=self.request.user.pk)

        return redirect("users:login")


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = "users/user_update.html"
    model = User
    form_class = UserUpdateForm

    def test_func(self):
        """
        Обновить информацию о пользователе может:
         - пользователь
         - суперпользователь
         - стафф
        """
        user_page_owner: User = self.get_object()
        user_request: User = self.request.user

        can_see_the_page: bool = (user_request.is_superuser or
                                  user_request.is_staff or
                                  user_request == user_page_owner)

        if can_see_the_page:
            return True
        return False

    def get_success_url(self):
        """Редирект на страницу о пользователе (UserDetailView)"""
        url = reverse_lazy("users:user", kwargs={"pk": self.request.user.pk})
        return url

    def handle_no_permission(self):
        """Если нет доступа, то вывод сообщения"""
        messages.error(request=self.request, message="У вас нет доступа к этой странице!")

        if self.request.user.is_authenticated:
            return redirect("users:user", pk=self.request.user.pk)

        return redirect("users:login")

# Todo - возможно тут вообще не нужен handle_no_permission. Иследовать этот момент
# Todo - написать миксин, в котором будет переопределен test_func, так как он повторяется в двух классах
