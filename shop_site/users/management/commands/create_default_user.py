from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    """
    Команда для создания стандартного пользователя.

    - Проверяет существование пользователя по email и телефону
    - Создаёт пользователя, если он отсутствует
    """
    help = "Создание стандартного пользователя (User Default)"

    def handle(self, *args, **options) -> None:
        """Основная логика выполнения команды."""

        username = "default_user"
        first_name = "User"
        last_name = "Default"
        email = "default_user@mail.ru"
        telephone = "89999999999"
        password = "default_user_password_1234"

        if (
                User.objects.filter(username=username).exists()
                or User.objects.filter(email=email).exists()
                or User.objects.filter(telephone=telephone).exists()):
            self.stdout.write(
                self.style.WARNING("Пользователь уже существует.")
            )
            return None

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
