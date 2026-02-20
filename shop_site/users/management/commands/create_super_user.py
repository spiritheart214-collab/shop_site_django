"""Модуль создает cупер пользователя для админки"""
from django.core.management.base import BaseCommand

from .config import User
from .utils import write_down_user, is_user


class Command(BaseCommand):
    """
    Команда для создания стандартного пользователя.

    - Проверяет существование пользователя по email и телефону
    - Создаёт пользователя, если он отсутствует
    """
    help = "Создание супер пользователя (User Super)"

    def handle(self, *args, **options) -> None:
        """Основная логика выполнения команды."""

        # Данные пользователя
        username = "super_user"
        first_name = "User"
        last_name = "Super"
        email = "super_user@mail.ru"
        telephone = "89998887777"
        password = "super_user_password"

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
        user = User.objects.create_superuser(
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

        # Запись данных о созданном пользователе в файл
        write_down_user(full_name=user.full_name, username=username, passwords=password)
