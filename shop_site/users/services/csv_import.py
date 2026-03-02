"""Модуль с реализующий парсинг импортируемого файла и создание пользователя на его основе"""
from csv import DictReader
from io import TextIOWrapper
from typing import Dict, List, Union

from django.core.files.uploadedfile import UploadedFile
from django.db import IntegrityError

from ..models import User


def parse_csv(uploaded_file: UploadedFile) -> List[Dict[str, str]]:
    """Читает CSV файл и превращает в список словарей"""
    csv_file = TextIOWrapper(uploaded_file, encoding="utf-8")
    csv_reader: List[Dict[str, str]] = list(DictReader(csv_file))
    return csv_reader


def create_users(users_list: List[Dict[str, str]]) -> Dict[str, Union[int, str]]:
    """
    Создаёт пользователей из списка словарей.

    Возвращает:
        tuple:
            - количество успешно созданных пользователей
            - список ошибок
    """
    print(users_list)
    success_count: int = int()
    errors: List[str] = list()

    for index, user in enumerate(users_list, start=1):
        print(index)
        print(user)

        try:
            User.objects.create_user(
                username=user.get("username"),
                first_name=user.get("first_name"),
                last_name=user.get("last_name"),
                email=user.get("email") or None,
                telephone=user.get("telephone") or None,
                password=user.get("password") or "default123"
            )
            success_count += 1
        except IntegrityError as error:
            errors.append(f"Строка: {index}\n"
                          f"Ошибка: {str(error)}")
        except Exception as error:
            errors.append(f"Строка {index}: {str(error)}")

    users_data = {
        "success": success_count,
        "errors": errors
    }

    return users_data
    # Todo добавить сервис перевода для ошибок ?!
