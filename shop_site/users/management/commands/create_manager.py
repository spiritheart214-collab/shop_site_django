"""Модуль создает manager'a для админки"""
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from .config import User
from .utils import write_down_user, is_user


class Command(BaseCommand):
    """
    Команда для создания менеджера.

    - Проверяет существование менеджер по email и телефону
    - Создаёт менеджера, если он отсутствует
    - Наделяет прававами по просмотру/добавлению/редактированию пользователей
    """
    help = "Создание менеджера (Manager Default)"

    def handle(self, *args, **options) -> None:
        """Основная логика выполнения команды."""

        # Данные пользователя
        username = "default_manager"
        first_name = "Manager"
        last_name = "Default"
        email = "default_manager@mail.ru"
        telephone = "88888888888"
        password = "manager_password_1234"

        # Существует ли такой пользователь
        if is_user(username=username, email=email, telephone=telephone):
            self.stdout.write(
                self.style.WARNING("Пользователь уже существует.")
            )

            self.stdout.write(
                self.style.SUCCESS(f"\tЛогин: {username}\n"
                                   f"\tПороль: {password}")
            )

            return None
        # Создание пользователя
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            telephone=telephone,
            password=password
        )

        self.stdout.write(
            self.style.SUCCESS(f"Пользователь {user.full_name} успешно создан.")
        )

        self.stdout.write(
            self.style.SUCCESS(f"Логин: {username}\n"
                               f"Пороль: {password}")
        )

        # Назначение прав
        content_type = ContentType.objects.get_for_model(User)

        view_permission = Permission.objects.get(
            content_type=content_type,
            codename='view_user'
        )

        change_permission = Permission.objects.get(
            content_type=content_type,
            codename='change_user'
        )

        add_permission = Permission.objects.get(
            content_type=content_type,
            codename='add_user'
        )

        delete_permission = Permission.objects.get(
            content_type=content_type,
            codename='delete_user'
        )

        user.user_permissions.add(view_permission, change_permission, add_permission, delete_permission)
        user.is_staff = True
        user.save()

        permissions_text = (f"Права менеджера:\n"
                            f"\t- Добавлять пользователей\n"
                            f"\t- Удалять пользователей\n"
                            f"\t- Редактировать пользователей\n"
                            f"\t- Просматривать пользователей")

        self.stdout.write(
            self.style.SUCCESS(permissions_text)
        )

        # Запись данных о созданном пользователе в файл
        write_down_user(full_name=user.full_name, username=username, passwords=password, extra_text=permissions_text)
