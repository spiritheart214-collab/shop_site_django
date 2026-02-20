import os
from typing import Optional

from django.conf import settings

from .config import User


def write_down_user(full_name: str, username: str, passwords: str, extra_text: Optional[str] = None) -> None:
    """
    Записывает дынне пользователя в файл.

    - Создает отдельную папку для хранения записей (если еще не создана)
    - Запсывает полное имя, логин и пороль пользователя


    :param full_name:  Полное имя пользователя
    :param username: логин
    :param passwords: пороль
    :param extra_text: дополнительное сообщение
    """

    users_info_dir = os.path.join(settings.BASE_DIR, "users", "management", "users_logins_passwords")
    users_info_file = os.path.join(users_info_dir, "logins_passwords.txt")

    os.makedirs(users_info_dir, exist_ok=True)

    with open(users_info_file, "a", encoding="utf-8") as my_file:
        my_file.write(f"{'=' * 50}\n")
        my_file.write(f"Пользователь: {full_name}\n")
        my_file.write(f"\tЛогин: {username}\n")
        my_file.write(f"\tПороль: {passwords}\n")
        if extra_text is not None:
            my_file.write(extra_text)

        my_file.write(f"\n\n\n")


def is_user(username: str, email: str, telephone: str) -> bool:
    """
    Проверка на существование пользователя в базе данных по уникальным полям

    :param username: никнейм пользователя
    :param email: email
    :param telephone: телефон
    :return:
    """
    if (
            User.objects.filter(username=username).exists()
            or User.objects.filter(email=email).exists()
            or User.objects.filter(telephone=telephone).exists()):
        return True
    return False
