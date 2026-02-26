"""Модуль с вспомогательными миксинами для view"""
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy

from .models import User


class UserAccessMixin(UserPassesTestMixin):
    """
    Миксин для проверки доступа к объекту пользователя.

    Доступ разрешён:
        - владельцу
        - суперпользователю
        - staff-пользователю

    Работает только с view, где доступен объект (get_object), например DetailView и UpdateView.
    """
    permission_denied_message = "У вас нет доступа к этой странице!"

    def test_func(self) -> bool:
        """
        Обновить информацию о пользователе может:
         - пользователь
         - суперпользователь
         - стафф
        """
        owner: User = self.get_object()
        user: User = self.request.user

        can_see_the_page: bool = self.has_permission(user=user, owner=owner)

        if can_see_the_page:
            return True
        return False

    def handle_no_permission(self) -> HttpResponseRedirect:
        """Если нет доступа, то вывод сообщения"""
        messages.error(request=self.request, message=self.permission_denied_message)

        if self.request.user.is_authenticated:
            return redirect("users:user", pk=self.request.user.pk)

        return redirect("users:login")

    def has_permission(self, user: User, owner: User) -> bool:
        """
        Проверка прав.
        Возвращает True если пользователь - супепрпользователь/администратор/владелец страницы.

        :param user: Пользователь переходящйий нас страницу
        :param owner: Оригинальный владелец страницы
        :return: bool
        """
        is_has_permission = user.is_superuser or user.is_staff or user == owner
        return is_has_permission


class UserSuccessUrlMixin:
    """
    Миксин для редиректа на страницу пользователя после успешного действия.

    Требования:
        - во view должен быть self.request.user
    """
    def get_success_url(self) -> str:
        """Редирект на страницу о пользователе (UserDetailView)"""
        user: User = getattr(self, "object", None) or self.request.user
        url = reverse_lazy("users:user", kwargs={"pk": user.pk})
        return url
